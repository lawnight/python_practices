# -*- coding: utf-8 -*-
import xxtea
import hexdump
import settings
import si
import zlib
import json

def dump(src, length=16):
    hexdump.hexdump(src)
    # result = []
    # digits = 4 if isinstance(src, unicode) else 2
    # for i in xrange(0, len(src), length):
    #     s = src[i:i + length]
    #     hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
    #     text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
    #     result.append(b"%04X   %-*s   %s" %
    #                   (i, length * (digits + 1), hexa, text))
    # print(b'\n'.join(result))

#一个index，4个字节
def getIntByIndex(buffer, index):
    bf = buffer[index * 4:index * 4 + 4]
    # pyton2
    # bf = bf[::-1]
    # bf = bf.encode('hex')
    # return int(bf, 16)
    # python3
    return int.from_bytes(bf, 'little')

def revertStr(num):
    return str("%x" % num).decode('hex')

def getBuf(buffer, offset):
    bf = buffer[offset:offset + 4]
    return bf

# 解码
def decrypt(data, key):
    if len(data) <= 3:
        return data
    # data length is not a multiple of 4, or less than 8.
    padding = len(data) // 4 * 4
    to_data = data[0:padding]
    # print 'data' + str(len(data))
    # print 'to_data:' + str(len(to_data))
    plain = ''
    plain = xxtea.decrypt(to_data, key,False)
    if padding < len(data):
        plain = plain + data[padding::]
    return plain

# 加密
def encrypt(data, key):
    if len(data) <= 3:
        return data
    padding = len(data) / 4 * 4
    to_data = data[0:padding]
    cipher = xxtea.encrypt(to_data, key,False)
    if padding < len(data):
        cipher = cipher + data[padding::]
    return cipher


def handler(buffer,rand_key):
    # 包头 msgId(4) Length(4) seq(4) crc(4) compressType(1)    
    headLen = 21
    receiveLen = len(buffer)
    if receiveLen>=headLen:
        msgId = getIntByIndex(buffer, 0)        # messageid
        sourceLen  = getIntByIndex(buffer, 1)  # sourceLength 包括包头
        seq = getIntByIndex(buffer, 2)
        crc = getIntByIndex(buffer, 3)         # crc 第4个
        compressType = int.from_bytes(buffer[16:17], 'little')       
        key = rand_key + getBuf(buffer, 0) + getBuf(buffer,
                                                        4 * 4 + 1) + getBuf(buffer, 3 * 4)
        # print (key,len(key))
        # print (rand_key,len(rand_key))
        # print ("sourceLen" + str(sourceLen))
        # cache没有接收完全的包
        if sourceLen > receiveLen:
            return
        datalen = sourceLen - headLen
        #游戏数据大于等于8个字节，才会加密
        print("msgId:",msgId,"len:",sourceLen,"seq:",seq) 
        source = buffer[headLen:(datalen + headLen)]
        if datalen >= 8:
            source = decrypt(source, key)  
            if compressType==1:
                # 解压缩             
                source = zlib.decompress(source)
        # 输出信息
        # if settings.filter_msgId and settings.filter_msgId == msgId:
        if settings.detail:
            if settings.dump:
                dump(buffer[0:headLen] + source)
                print(source)
            # 解析si的具体信息
            if len(source)>0:
                si.show_si(source)
            # dump(source)
       
         # 返回完整的包
        return si.Packet(msgId,sourceLen,buffer[0:headLen] + source)
