# -*- coding: utf-8 -*-
# 分析si协议包。
# todolist:1：部分不常用si协议类型没实现 2：多session管理 3：协议的图表分析 4：输出美观

from scapy.all import *
import decode
import pyshark
from Session import *
import settings
session = None
def getSession(src,dst):
    global session
    if not session:        
        session = Session(src,dst)
        return session
    return session
    

def packet_scapy(packet):
        #print packet.show()
        # 数据包长度大于40才有数据携带    
    if packet[IP].len>40 and packet[TCP].payload: 
        # python2
        # game_packet = str(packet[TCP].payload)
        # 去掉padding
        game_packet = packet[TCP].load
        src = packet[IP].src
        dst = packet[IP].dst
        session_key = "[%-15s]>>>>>>>>>>>>[%s]" % (src,dst)  
        print(session_key)
        session = getSession(src,dst)  
        session.receiveBuf(src,game_packet)
        # decode.handler(session_key,game_packet)
        # wrpcap('filtered.pcap', packet, append=True)


print('开始抓包……%s'%(datetime.now()))
if settings.mode == 'sniff':
    packets = sniff(filter="tcp port 10001",prn=packet_scapy,store=0)
else:
    pkts = rdpcap(settings.fileName)
    port = settings.port
    filter_pkts = pkts.filter(lambda x:TCP in x and (x[TCP].sport == port  or x[TCP].dport == port))
    for pkt in filter_pkts:
        # pkt.show()
        packet_scapy(pkt)
    # filter_pkts.plot()
print("结束抓包")