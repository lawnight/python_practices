# -*- coding: utf-8 -*-
# si 结构的解码
from enum import Enum
import struct
import zlib
import xxtea
import hexdump
import settings
from scapy.all import *

headLen = 21

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

class Packet(object):
    # 内容
    buf = ''
    # 协议id
    msgId = 0
    # 长度
    length = 0
    seq = 0
    crc = 0
    compressType = 0    

    def __init__(self,msgId,length,buffer,time):
        self.msgId = msgId
        # 原来包的大小（解密，解压前）
        self.length = length
        self.buf=buffer    
        self.seq = getIntByIndex(buffer, 2)
        self.crc = getIntByIndex(buffer, 3)         # crc 第4个
        self.compressType = int.from_bytes(buffer[16:17], 'little')  
        self.time = time
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
# 包头 msgId(4) Length(4) seq(4) crc(4) compressType(1)    
#si具体结构    int类型 1010|0000  前四位代表类型，后四位代表int占用的字节。 1010|1111 占用四个字节的int
# /** 心跳请求消息id */
# public static final int REQUEST_HEARTBEAT = 0;
# /** 心跳响应消息id */
# public static final int RESPONSE_HEARTBEAT = 1;
# /** 生成编解码key请求消息id */
# public static final int REQUEST_GENERATE_ENCODE_KEY = 2;
# /** 生成编解码key响应消息id */
# public static final int RESPONSE_GENERATE_ENCODE_KEY = 3;
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
         (self.data)

# 双向链接 (因为公用一个密钥，所以放在一起)
class Session():
    def __init__(self,key):
        src,dst = key.split('||')
        self.aIP=src
        self.bIP=dst  
        self.bufs={}    # 缓存的buff数据   
        self.bufs[src] = b''
        self.bufs[dst] = b''
        self.pkts = []
        self.randKey = b'0000'
    
    def getPacket(self,buffer,time):        
        headLen = 21
        receiveLen = len(buffer)
        if receiveLen>=headLen:            
            packetLen  = getIntByIndex(buffer, 1)   # packetLen 包括包头            
            if packetLen > receiveLen:
                return
            msgId = getIntByIndex(buffer, 0)        # messageid            
            seq = getIntByIndex(buffer, 2)            
            datalen = packetLen - headLen         
               
            # print("msgId:",msgId,"len:",packetLen,"seq:",seq) 
            source = buffer[headLen:(datalen + headLen)]
            # 返回完整的包
            return Packet(msgId,packetLen,buffer[0:headLen] + source,time)
    
    def show(self):
        print(self.aIP,self.bIP)        
        for p in self.pkts:           
            print('dump msg:',p.msgId,p.length)
            buf = decode_buf(p.buf,p.compressType,self.randKey)
            if settings.detail:
                if settings.dump:
                    dump(buf)                    
                # 解析si的具体信息
                source = buf[headLen::]
                if len(source)>0:
                    show_si(source)
    def show_brife(self):
        data = [",".join([str(x.msgId),str(x.seq)]) for x in self.pkts]
        print(len(data))
        print(data)
    def receiveBuf(self,srcIp,buf,time):  
        if self.bufs[srcIp] != None:
            self.bufs[srcIp] = self.bufs[srcIp] + buf  
            print(self.aIP,self.bIP)            
            pkt =self.getPacket(self.bufs[srcIp],time) # decode.handler(self.bufs[srcIp],self.randKey) #   
            if pkt:                   
                if pkt.msgId == 3:   
                    key = pkt.buf[22:22 + 4]
                    length = len(key)
                    # key需要补足4个字节
                    self.randKey =  key   + b'\x00' * (4 - length)
                #去掉解析后的包
                self.bufs[srcIp] = self.bufs[srcIp][pkt.length::]
                # 记录包
                self.pkts.append(pkt)
    def getLine(self):
        s = pd.Series((x.length for x in s.pkts),index=(x.time for x in s.pkts))
        s.index = pd.to_datetime(s.index,unit='s')
        return s

#一个index，4个字节
def getIntByIndex(buffer, index):
    bf = buffer[index * 4:index * 4 + 4]
    return int.from_bytes(bf, 'little')

def getBuf(buffer, offset):
    bf = buffer[offset:offset + 4]
    return bf

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

def dump(src, length=16):
    hexdump.hexdump(src)

sessionMap = {}
def getSession(key):
    global sessionMap   
    if key in sessionMap.keys():    
        session = sessionMap[key]
    else:
        
        session = Session(key)
        sessionMap[key] = session
    return session

# src->dst
def receive(packet,time):
    ip_src_fmt = "{IP:%IP.src%}{IPv6:%IPv6.src%}"
    ip_dst_fmt = "{IP:%IP.dst%}{IPv6:%IPv6.dst%}"
    addr_fmt = (ip_src_fmt, ip_dst_fmt)
    fmt = "{}:%r,TCP.sport% || {}:%r,TCP.dport%"

    key = packet.sprintf(fmt.format(*addr_fmt))
    src,dst = key.split('||')
    src,dst = src.strip(),dst.strip()
    session_key = ''
    if src < dst:
        session_key = src + "||" + dst
    else:
        session_key = dst + "||" + src
    # print('src [%s]'%src)
    # print('dst [%s]'%dst)
    # print('session_key',session_key)
    session = getSession(session_key)

    game_packet = packet[TCP].load
    session.receiveBuf(src,game_packet,time)

def decode_buf(buf,compressType,rkey):
    datalen = len(buf) - headLen
    source = buf[headLen:(datalen + headLen)]
    if datalen >= 8:
        rkey = rkey + getBuf(buf, 0) + getBuf(buf,4 * 4 + 1) + getBuf(buf, 3 * 4)
        source = decrypt(source, rkey)  
        if compressType==1:
            # 解压缩             
            source = zlib.decompress(source)
    return buf[0:headLen] + source


def show_si(buf):
    detail = Struct_si(buf)
    data = detail.read()
    while data != None:
        # js = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
        print(data)
        data = detail.read()

# b = b'\xa5.\xf2#\x05%\xc2;|\x8e\xd0e\xadO_NG\x1b,n8\xe6\x9d\xf8\xb93\x93\x1bQ\x03P'
# a = Struct_si(b)
# a.read()