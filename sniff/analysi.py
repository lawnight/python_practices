import pandas as pd
import matplotlib.pyplot as plt
import si
import re
from collections import defaultdict

def analysi():
    # 分析协议频繁度
    dd = [] # 不分session的所有包
    for d in si.sessionMap:
        se = si.sessionMap[d] # se 代表session
        dd = dd + list(se.pkts)
    pg,ax = plt.subplots(2,2)    
    (ax1,ax2),(ax3,ax4)= ax
    # value是协议号，协议号的频繁度
    series = pd.Series([x.msgId for x in dd])
    series.value_counts().drop([0,1,2,3])[:10].plot(kind='bar',ax = ax1)
    ax1.set_xlabel('协议号')
    ax1.set_title('协议频繁度')

    # 分析响应时间
    result = {}
    for d in si.sessionMap:
        se = si.sessionMap[d] # se 代表session
        data = defaultdict(list)
        for d in se.pkts:
            if d.msgId==0 or d.msgId==1:
                continue
            data[d.msgId].append(d.time)

        data = pd.DataFrame.from_dict(data,orient='index')
        idx = data.index
        pairs = getCodePair()
        
        for pair in pairs:
            c_code,s_code = pair
            if c_code not in idx or s_code not in idx:
                # print('不包含协议',c_code,s_code)
                continue
            s_ser =  data.loc[s_code].dropna()
            c_cer =  data.loc[c_code].dropna()
            if len(s_ser) != len(c_cer):
                # print('长度不一样',pair)
                continue
            # print('包含',c_code,s_code,len(data.loc[c_code]),len(data.loc[s_code]))
            value = (s_ser - c_cer).mean()*1000
            if(value > 1000):
                print('异常延时：','||'.join([se.aIP,se.bIP]),pair)
                continue
            pair = str(c_code)
            if pair in result.keys():
                result[pair] = (result[pair]+ value)/2
            else:
                result[pair] = value
            # 缺失或不能匹配的协议
    del result[str(2901)]
    del result[str(2902)]
    print('总{}对协议，有数据统计{}对'.format(len(pairs),len(result)))
    s = pd.Series(result)
    s.sort_values(ascending=False)[:10].plot(ax=ax2,kind='bar')

    # 协议压缩率
    # series = pd.Series([x.length for x in dd],index = [x.msgId for x in dd])
    series = pd.Series([x.compressType for x in dd],index = [x.msgId for x in dd])
    series.value_counts().plot(kind='pie',ax = ax3)
    ori_len = 0
    decoded_len = 0
    for d in si.sessionMap:
        se = si.sessionMap[d]
        for pk in se.pkts:
            if pk.compressType==1:
                ori_len = ori_len + pk.length
                newBuf = si.decode_buf(pk.buf,pk.compressType,se.randKey)
                decoded_len = decoded_len + len(newBuf)
    ax3.set_title('压缩率为:%f'%(ori_len/decoded_len))
        

# data.loc[805].dropna() - data.loc[802].dropna()
    # 分析
def getCodePair(): 
    result = []
    with open('/Users/near/work/war_mix_server/server/src/main/java/com/xd100/sg/net/ModuleId.java','rt') as f:
        data = f.read()
        resRe = re.findall('public final static int (.*?response.*?) .*?(\d*);',data)
        reqRe = re.findall('public final static int (.*?request.*?) .*?(\d*);',data)
        # 配对        
        for a in reqRe:
            aSign,aCode = a
            aSign = aSign.replace('request','response')
            for b in resRe:
                bSign,bCode = b
                if aSign == bSign:
                    result.append((int(aCode),int(bCode)))
        
    return result

