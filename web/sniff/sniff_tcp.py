# -*- coding: utf-8 -*-
# 分析si协议包。
# todolist:1：部分不常用si协议类型没实现  4：输出美观
from scapy.all import *
import pyshark
import settings
from importlib import reload
import pandas as pd
import matplotlib.pyplot as plt
import si
import analysi
def packet_scapy(packet):
        #print packet.show()
        # 数据包长度大于40才有数据携带    
    if packet[IP].len>40 and packet[TCP].payload: 
        # python2
        # game_packet = str(packet[TCP].payload)
        # 去掉padding
       
        src = packet[IP].src
        dst = packet[IP].dst
        session_key = "[%-15s]>>>>>>>>>>>>[%s]" % (src,dst)  
        sPort = packet[TCP].sport
        dPort = packet[TCP].dport

        game_packet = packet[TCP].load
        si.receive(src,sPort,dst,dPort,game_packet,packet.time)

print('开始抓包……%s'%(datetime.now()))

def anlysis(fileName,port):
    pkts = rdpcap(fileName)       
    # and (x[IP].src=='192.168.101.60' or x[IP].dst == '192.168.101.60') 
    filter_pkts = pkts.filter(lambda x:TCP in x and (x[TCP].sport == port  or x[TCP].dport == port) )
    for pkt in filter_pkts:
        packet_scapy(pkt)
            

print("结束抓包")
if settings.mode == 'sniff':
    packets = sniff(filter="tcp port 10001",prn=packet_scapy,store=0)
else:
    anlysis(settings.fileName,settings.port)
    # for v in si.sessionMap.values():
    #     v.show_brife()
    analysi.analysi()
# 平均响应时间
    
# 开始绘图
def drawLogin():
    anlysis("/Users/near/war.pcapng",10001)
    for s in si.sessionMap.values():
        s1 = s.getLine()
    anlysis("/Users/near/work/qs.pcapng",20001)
    for s in si.sessionMap.values():
        s2 = s.getLine()
    # 时间对齐
    delay = s1.index[0] - s2.index[0] 
    s2.index = s2.index + delay    
    print('开始绘图')
    s1.plot(ax=ax3,label='战国登录')
    ax = s2.plot(ax=ax3,label='茜色登录')
    ax3.legend(loc='best')

    anlysis("/Users/near/war.pcapng",10001)
    for s in si.sessionMap.values():
        s1 = getLine(s)
    anlysis("/Users/near/work/qs.pcapng",20001)
    for s in si.sessionMap.values():
        s2 = getLine(s)
    # 时间对齐
    delay = s.index[0] - s2.index[0] 
    s2.index = s2.index + delay


