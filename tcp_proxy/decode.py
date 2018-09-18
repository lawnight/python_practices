# -*- coding: utf-8 -*-
import xxtea

rand_key = '0000'

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i + length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X   %-*s   %s" %
                      (i, length * (digits + 1), hexa, text))
    print b'\n'.join(result)

#一个index，4个字节
def getIntByIndex(buffer, index):
    bf = buffer[index * 4:index * 4 + 4]
    bf = bf[::-1]
    bf = bf.encode('hex')
    return int(bf, 16)

#偏移offset个字节
def getIntByOffset(buffer, offset):
    bf = buffer[offset:offset + 4]
    bf = bf[::-1]
    bf = bf.encode('hex')
    return int(bf, 16)


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
    padding = len(data) / 4 * 4
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

def handler(buffer):
    # 包头 msgId(4) Length(4) seq(4) crc(4) compressType(1)
    msgId = getIntByIndex(buffer, 0)        # messageid
    sourceLen  = getIntByOffset(buffer, 4)  # sourceLength
    crc = getIntByIndex(buffer, 3)         # crc 第4个
    #key = _key + mesId+sourceLength+Crc
    global rand_key
    key = rand_key + getBuf(buffer, 0) + getBuf(buffer,
                                                      4 * 4 + 1) + getBuf(buffer, 3 * 4)
 
    # print "key:" + key.encode('hex')
    # print 'rand_key' + rand_key.encode('hex')
    # print ("sourceLen" + str(sourceLen))

    datalen = sourceLen - 21
    if datalen > 8:
        data = buffer[21:datalen + 21]
        source = decrypt(data, key) 
        print("msgId:",msgId,"len:",sourceLen)       
        hexdump(buffer[0:21] + source)
    return buffer
