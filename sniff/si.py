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
            data.append(value)
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
            data[SType(idx).name] = value
            return value
    def show(self):
        print(self.data)

def a(b):
    print(b)