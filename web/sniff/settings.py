# 有file和sniff两种模式
mode = "file"
# 分析文件，需要的参数
# 浅色
# fileName =  '/Users/near/work/qs.pcapng'
# port = 20001
# 战国
# fileName = '/Users/near/war.pcapng'
fileName = '/Users/near/Downloads/server (2).pcap'
# fileName = '/Users/near/Downloads/server.pcap'

# 需要关注的端口
port = 10001
#打印包的具体字节
detail = True
# 是否dump 二进制
dump = True
# 过滤的msgid
filter_msgId = 2209