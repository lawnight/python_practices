samples = int(input())
# 两个序列的比较 （记录特征的序列 和 每帧序列）
record_hightest = {}
for sample in range(samples):
    frames = int(input())    
    record_features = {}
    for f in range(0,frames):
        features = []
        s = list(map(int,input().split()))
        c,v =s[0],s[1:]    
        if c>0:
            for i in range(0,c):
                features.append((v[i*2],v[i*2+1]))
        for feat in features:
            if feat in record_features:
                record_features[feat] = record_features[feat] + 1
            else:
                record_features[feat] = 1
        #处理没有连续的
        for k in list(record_features.keys()):
            if not k in features:                
                if k in record_hightest:
                    if record_hightest[k] < record_features[k]:
                        record_hightest[k] = record_features[k]
                else:
                    record_hightest[k] = record_features[k]
                # remove
                record_features.pop(k)
    #最后一帧，记录最高的
    for k in record_features.keys():
        if k in record_hightest:
            if record_hightest[k] < record_features[k]:
                record_hightest[k] = record_features[k]
        else:
            record_hightest[k] = record_features[k]
        
maxV = 0
for k,v in record_hightest.items():
    if v>maxV:
        maxV = v
print(maxV)