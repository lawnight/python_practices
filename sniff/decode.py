# -*- coding: utf-8 -*-
import xxtea
import hexdump
import settings
import si
import struct
#两个字节的key
rand_key = b'0000'

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
    return str

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

# modify any responses destined for the local hosts

#回包
def response_handler(buffer):
    # perform packet modifications
    int2 = getIntByIndex(buffer, 0)  # messageid
    # global rand_key
    # random key
    if(int2 == 3):
        rand_key = getBuf(buffer, 22)
        # print 'rand_key:' + rand_key.encode('hex')
    return buffer

cacheBuffer = b''
#si具体结构    int类型 1010|0000  前四位代表类型，后四位代表int占用的字节。 1010|1111 占用四个字节的int

def handler(buffer):
    # 包头 msgId(4) Length(4) seq(4) crc(4) compressType(1)    
    headLen = 21    
    global cacheBuffer
    cacheBuffer = cacheBuffer + buffer
    receiveLen = len(cacheBuffer)
    if receiveLen>=headLen:
        msgId = getIntByIndex(cacheBuffer, 0)        # messageid
        sourceLen  = getIntByIndex(cacheBuffer, 1)  # sourceLength 包括包头
        crc = getIntByIndex(cacheBuffer, 3)         # crc 第4个
        #key = _key + mesId+sourceLength+Crc
        global rand_key
        key = rand_key + getBuf(cacheBuffer, 0) + getBuf(cacheBuffer,
                                                        4 * 4 + 1) + getBuf(cacheBuffer, 3 * 4)
        # print "key:" + key.encode('hex')
        # print 'rand_key' + rand_key.encode('hex')
        # print ("sourceLen" + str(sourceLen))
        # cache没有接收完全的包
        if sourceLen > receiveLen:            
            cacheBuffer = cacheBuffer
            return
        datalen = sourceLen - headLen
        #游戏数据大于8个字节，才会加密
        print("msgId:",msgId,"len:",sourceLen) 
        source = cacheBuffer[headLen:datalen + headLen]
        if datalen > 8:
            source = decrypt(source, key)  
        if settings.detail:
            dump(cacheBuffer[0:headLen] + source)
            si.decode_si(source)
            # dump(source)
        if msgId == 3:        
            rand_key = getBuf(buffer, 22)
            print('rand_key',rand_key)
        #去掉解析后的包
        cacheBuffer = cacheBuffer[sourceLen::]
         # 服务器发送的密钥
        return source