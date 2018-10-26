# -*- coding: utf-8 -*-
from scapy.all import *
import decode
import pyshark
count = 0
def packet_scapy(packet):
    #print packet.show()
    # 有数据携带
    try:
        if packet[IP].len>40 and packet[TCP].payload: 
                # python2
                # game_packet = str(packet[TCP].payload)
                # 去掉padding
                game_packet = packet[TCP].load        
                print("[%-15s]>>>>>>>>>>>>[%s]" % (packet[IP].src,packet[IP].dst))
                decode.handler(game_packet)
                global count 
                count = count +1
                # wrpcap('filtered.pcap', packet, append=True)
    except Exception as e:
            print(e)
    

print('开始抓包……%s'%(datetime.now()))
packets = sniff(filter="tcp port 10001",prn=packet_scapy,store=0)
# pkts = rdpcap("/Users/near/work/qs.pcapng")

pkts = rdpcap("/Users/near/war.pcapng")
filter_pkts = pkts.filter(lambda x:TCP in x and (x[TCP].sport == 10001 or x[TCP].dport == 10001))

for pkt in filter_pkts:
        # pkt.show()
        packet_scapy(pkt)
print('登录前交互数%d'%count)       
# filter_pkts.plot()
print("结束抓包")