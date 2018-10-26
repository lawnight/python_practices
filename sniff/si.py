# -*- coding: utf-8 -*-
# si 结构的解码
from enum import Enum
import struct

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
    def readByte(self):       
        # 如果a[0]是返回int bytes是int的序列 
        data = self.buf[self.idx:self.idx+1]
        self.idx = self.idx + 1
        return data        

class Struct_si():
    buf = None
    def __init__(self, _pkt=b""):
        self.buf = ByteStream(_pkt)
    def hasValue(self,identity,index):
        return (identity & (0x01 << index)) != 0
    def getIdentity(self):
        return self.buf.readByte()[0]
    def readUnsignedInt(self,identity):
        data = b''
        for i in range(4):
            if (self.hasValue(identity, i)): 
                data = data + self.buf.readByte()
        print(data)
        value = struct.unpack('I',data)
        print("int",value,type(value))
        return value
    def readInt(self,identity):        
        data = b''
        for i in range(4):
            if (self.hasValue(identity, i)): 
                data = data + self.buf.readByte()
        print(data)
        value = struct.unpack('i',data)
        print("int",value,type(value))
        return value
    def readSMap(self,identity):
        self.readUnsignedInt()
        length = self.readUnsignedInt()
        for i in range(length):
            key  = self.read()
            value = self.read()
    def read(self):
        identity = self.getIdentity()
        idx = identity & 0xf0
        if idx==SType['Int'].value:           
            return self.readInt(identity)
        if idx==SType['Map'].value:
            print("map")
        if idx==SType['UnsignedInt'].value:
            return self.readUnsignedInt(identity)

# b'\x5f\xff\xff\xff\xff'
a = Struct_si(bytes.fromhex('5fffffffff'))
a.read()