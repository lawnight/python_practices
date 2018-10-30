import decode
# 双端sesstion
class Session():
    aIP = ''
    bIP = ''
    aBuf = b''
    bBuf = b''
    bufs = {}
    pkts = []

    def __init__(self,src,dst):
        self.aIP=src
        self.bIP=dst
        self.bufs[src] = b''
        self.bufs[dst] = b''

    def receiveBuf(self,srcIp,buf):  
        if self.bufs[srcIp] != None:
            self.bufs[srcIp] = self.bufs[srcIp] + buf
            pkt = decode.handler(self.bufs[srcIp])
            if pkt:
                #去掉解析后的包
                self.bufs[srcIp] = self.bufs[srcIp][len(pkt)::]
                # 记录包
                self.pkts.append(pkt)
        