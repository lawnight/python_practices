# -*- coding: utf-8 -*-
# si 结构的解码
from enum import Enum
import struct
import zlib

class SType (Enum):
    Boolean =0
    Byte = 1 << 4
    UnsignedByte = 2 << 4
    Short = 3 << 4
    UnsignedShort = 4 << 4
    Int = 5 << 4
    UnsignedInt = 6 << 4
    Float = 7 << 4
    Double =8 << 4
    Long = 9 << 4
    String = 10 << 4
    ByteArray = 11 << 4
    Map =12 << 4
    List=13 << 4

class ByteStream():
    buf = None
    idx = 0
    def __init__(self, _pkt=b""):
        self.buf = _pkt
    def readByte(self,length=1):
        if length:
            data = self.buf[self.idx:self.idx+length]
            self.idx = self.idx + length
        else:   
            # 如果a[0]是返回int bytes是int的序列 
            data = self.buf[self.idx:self.idx+1]
            self.idx = self.idx + 1
        return data 
    def hasData(self):
        return len(self.buf) > self.idx       

class Struct_si():
    buf = None    
    data = {}
    def __init__(self, _pkt=b""):
        self.buf = ByteStream(_pkt)        
    def hasValue(self,identity,index):
        return (identity & (0x01 << index)) != 0
    def getIdentity(self):
        if self.buf.hasData():     
            return self.buf.readByte()[0]
    def readByte(self,identity):
        value = 0
        if (self.hasValue(identity, 0)): 
            value |= ((self.buf.readByte()[0] & 0xff) << (0 << 3))
        return value

    def readUnsignedInt(self,identity = 0):        
        value = 0
        for i in range(4):
            if (self.hasValue(identity, i)): 
                value |= ((self.buf.readByte()[0] & 0xff) << (i << 3))
        return value
    
    def tryReadUnsignedInt(self):
        identity = self.getIdentity()
        idx = identity & 0xf0
        if (idx == SType["UnsignedInt"].value):
            return self.readUnsignedInt(identity)
        

    def readInt(self,identity):
        value = 0
        for i in range(4):
            if (self.hasValue(identity, i)): 
                # data = data + self.buf.readByte()
                value |= ((self.buf.readByte()[0] & 0xff) << (i << 3))
        # python3 value是无符号的，需要转换成有符号的，变成负数
        temp = struct.pack('I',value)
        value = struct.unpack('i',temp)
        return value[0]
    def readLong(self,identity):
        identity = self.getIdentity()
        value = 0
        for i in range(8):
            if (self.hasValue(identity, i)): 
                # data = data + self.buf.readByte()
                value |= ((self.buf.readByte()[0] & 0xff) << (i << 3))
        # python3 value是无符号的，需要转换成有符号的，变成负数
        temp = struct.pack('L',value)
        value = struct.unpack('l',temp)
        return value[0]
    def readShort(self,identity):
        value = 0
        for i in range(2):
            if (self.hasValue(identity, i)): 
                # data = data + self.buf.readByte()
                value |= ((self.buf.readByte()[0] & 0xff) << (i << 3))
        # python3 value是无符号的，需要转换成有符号的，变成负数
        temp = struct.pack('H',value)
        value = struct.unpack('h',temp)
        return value[0]

    def readString(self,identity):
        length = self.readUnsignedInt(identity)
        if (length > 0):
            data = self.buf.readByte(length)
            return data.decode("utf-8")
    def readList(self,identity):
        data = []
        self.tryReadUnsignedInt()
        length = self.tryReadUnsignedInt()
        for i in range(length):
            data.append(self.read())
        return data
    def readSMap(self,identity):
        data = []
        self.tryReadUnsignedInt()
        length = self.tryReadUnsignedInt()
        for i in range(length):
            key  = self.read()
            value = self.read()
            data.append({"value":value})
        return data
    def readFloat(self,identity):
        value = 0
        for i in range(4):
                # data = data + self.buf.readByte()
                value |= ((self.buf.readByte()[0] & 0xff) << (i << 3))
        # python3 value是无符号的，需要转换成有符号的，变成负数
        temp = struct.pack('I',value)
        value = struct.unpack('i',temp)
        return value[0]
    def read(self):
        identity = self.getIdentity()       
        data = {}
        if identity:
            idx = identity & 0xf0
            value = ''
            if idx==SType['Int'].value:           
                value = self.readInt(identity)
            if idx==SType['Map'].value:
                value = self.readSMap(identity)                
            if idx==SType['UnsignedInt'].value:
                value =  self.readUnsignedInt(identity)
            if idx==SType['List'].value:
                value =  self.readList(identity)
            if idx==SType['String'].value:
                value = self.readString(identity)  
            if idx==SType['Long'].value:
                value =  self.readLong(identity)
            if idx==SType['Short'].value:
                value =  self.readShort(identity)    
            if idx==SType['Float'].value:
                value =  self.readFloat(identity) 
            if idx==SType['Byte'].value:
                value =  self.readByte(identity)        
            data[SType(idx)] = value
            return data
    def show(self):
        print(self.data)

def a(b):
    print(b)
# b'\x5f\xff\xff\xff\xff'
# buf = b'x\x9c[\xc8\xe2\x19\xe2\xea{!Y\x961\x91\xed@\xa2V"k \xe3\x81D\xceD\xa6@\xc6@\x81@\xa6`_\xfe@\xa6\x85,\xc9\xd9\x06F\x81\xcc\x13\x18\xd9\x02Y&\xd8[\xccxS\x9a\xc6\x18\xc8\xca\x88E\xb9\x1fXyV\x85\x811H\xb9\x11Hy\xe92\xdc\xca\xfda\xca\x8d\xe0\xca\xcb\xf1(\x0f\x80)7\x84+\xaf\xc2\xa3<\x06\xac\xbc\x18\xaa\x9c\x13\xa4\xfc\xe2G\xb8r]t\xe5\xf1 \xe5\xec\x99%\x96 \x00\xd2\xc1\x08\xd2q\xa4\xd3u\x01X\x07#\x00\xcd\xa5Q\xbc'
# buf = b'\xd1`{\xb3* \x08wk1g$\xae\xb3"U\x83\x93/\xb5\x82\x8c\x90H\x91\xad\xf2\xa0O\xe5,,3f\xa6hB\x05\x97\xc4(\xc6X\xabv\xaf"\xfa\xbb\xabKR\xaa<x{z#\xc4e\x88\xca\xf0n\x1fs\xe3\xbf]\x04\x91\xe1\xa5d\xceG.\xd3\x00\xd5\x0f\xf8\xa1\xeb,[\\\x9c2*\x0c\xe3\x8f\xeb\xfa\x00zl\x18[[6p\x8d\xb8I\x7f\xd3\xf1\x036\x91\xfbL\x1f\x15\x91RT\xf6\xda\x8bR\xd0\x85\xa9\xdd\xdd\x94\x8f\xd5\x9f\x81\x06\xb6\xe6P \x9c6Q\xbc'
# a = Struct_si(bytes.fromhex('D0610261015103'))
# print(len(buf))
# print(buf)

# print(list(buf))

# buf = zlib.decompress(buf, zlib.MAX_WBITS | 16)

# a = Struct_si(buf)
# data = a.read()
# while data:
#     print(data)
#     data = a.read()
