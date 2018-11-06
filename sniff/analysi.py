import pandas as pd
import matplotlib.pyplot as plt
import si

def zipPercent(sessions):
    dd = []
    for d in si.sessionMap:
        se = si.sessionMap[d]
        dd = dd + list(se.pkts.values())
    pg,ax = plt.subplots(2,2)    
    # value是协议号，协议号的频繁度
    series = pd.Series([x.msgId for x in dd])
    series.value_counts().drop([0,1,2,3])[:10].plot(kind='bar',ax = ax[0][0])
    ax[0][0].set_xlabel('协议号')
    # 协议压缩率
    # series = pd.Series([x.length for x in dd],index = [x.msgId for x in dd])
    series = pd.Series([x.compressType for x in dd],index = [x.msgId for x in dd])
    ori_len = 0
    new_len = 0
    for d in si.sessionMap:
        se = si.sessionMap[d]
        for pk in se.pkts.values():
            if pk.compressType==1:
                print('*'*16)
                print(se.randKey)
                ori_len = ori_len + pk.length
                newBuf = si.decode_buf(pk.buf,pk.compressType,se.randKey)
                new_len = new_len + len(new_len)
    ax[0][1].set_title('压缩率为:%f'%(ori_len/new_len))