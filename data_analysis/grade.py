#%%
import pandas as pd
path = r'D:\资料\公务员'
key1 = '行政职业能力测验成绩'
key2 = '申论成绩'
#%%
def filterPosition(df,role = '2020年高校应届毕业生和符合职位要求的社会在职、非在职人员',full = True,):
    """
    过滤满足条件的职位    
    """
     # 满足我的招录条件
    grade = '本科及以上'
    perfession = '计算机'
    level = '学士及以上'
    if full:
        level =level + '|无要求'
        perfession = perfession + '|不限'
        grade = grade + '|大专及以上'   
    df = df[df['招录对象'].str.contains(role+"|不限")]
    df = df[df['要求的学历'].str.contains(grade) ]
    df=df[df['专业'].str.contains(perfession)]
    df = df[df['要求的学位'].str.contains(level)]
    return df
def mergePosition(df,df2):
    df3 = pd.merge(df,df2,on='职位编码',how='left')
    return df3

def analysisLocation(a1,a2,key1 = 'sum',key2 = '名额'):
    """
    根据地点（招录机关）统计分数段
    key1:笔试分数
    key2:招录人数
    """

    b1 = a1.groupby('招录机关').agg({key1:['max','min','mean'],key2:['sum']})
    b2 = a2.groupby('招录机关').agg({key1:['max','min','mean'],key2:['sum']})
    r = pd.merge(b1,b2,on='招录机关',how='left')
    return r

df = pd.read_excel(os.path.join(path,'2018年上.xls'),skiprows=1)
df2 = pd.read_excel(os.path.join(path,'2018年下职位.xlsx'),skiprows=2)
df3 = mergePosition(df,df2)
a1 = filterPosition(df3,'2018年高校应届毕业生和符合职位要求的社会在职、非在职人员|具有两年以上基层工作经历的人员',True)
a2 = filterPosition(df3,'2018年高校应届毕业生和符合职位要求的社会在职、非在职人员|具有两年以上基层工作经历的人员',False)
analysisLocation(a1,a2,key1 = '笔试总成绩',key2= '录用名额')
# %%


def analysis(df,key1,key2):
    df['sum'] = df[key1] + df[key2]
    df['a'] = pd.cut(df[key1],range(0,200,5),right=False)
    df['b'] = pd.cut(df[key2],range(0,200,5),right=False)
    df['c'] = pd.cut(df['sum'],range(0,200,5),right=False)

    a_series = df.groupby('a').size()
    b_series = df.groupby('b').size()
    c_series = df.groupby('c').size()
    c = pd.DataFrame([a_series,b_series],index=['a','b'])
    # 去掉为0的项
    c = c.loc[:, (c != 0).any(axis=0)]
    #c.plot(kind='bar',stacked=True) 
    c_series.plot(kind='pie',autopct='%1.1f%%')

#%%
# %%
# d = r'D:\资料\公务员\2017年遂宁市检察系统招录公务员成绩汇总排名统计表.xls'
# df = pd.read_excel(d)
# analysis(df,key1,key2)