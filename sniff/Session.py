import decode
import pandas as pd
# 双端sesstion
class Session():
    aIP = ''
    bIP = ''
    aBuf = b''
    bBuf = b''
    # 缓存的buff数据
    bufs = {}
    # 需要分析的数据 time和包
    pkts = {}

    def __init__(self,src,dst):
        self.aIP=src
        self.bIP=dst        
        self.bufs[src] = b''
        self.bufs[dst] = b''
        self.pkts = {}

    def receiveBuf(self,srcIp,buf,time):  
        if self.bufs[srcIp] != None:
            self.bufs[srcIp] = self.bufs[srcIp] + buf
            pkt = decode.handler(self.bufs[srcIp])
            if pkt:
                #去掉解析后的包
                self.bufs[srcIp] = self.bufs[srcIp][len(pkt)::]
                # 记录包
                self.pkts[time] = len(pkt)

    def getLine(self):
        return self.pkts

        