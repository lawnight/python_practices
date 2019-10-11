#%%
import pandas as pd
import re

d = pd.read_excel(r"E:\side\1.xlsx",skiprows=3)
d2 = pd.read_excel(r"E:\side\2.xlsx")

# d2['职位编码'] = d2['职位名称(编号)'].apply(lambda x: int(re.findall(r'\((\d+)\)',x)[0]))

# c = pd.merge(d,d2,on='职位编码',how='left')



df1 = pd.concat(pd.read_excel(r'D:\code\br_mix_server\excel\common\ConfigValue.xlsx',sheet_name=None))

df2 = pd.concat(pd.read_excel(r'E:\ConfigValue.xlsx',sheet_name=None))

pd.concat([df1,df2]).drop_duplicates(keep=False)


import os
path = r'D:\code\war_mix_server\excel\topicStory\story_data'
l = [x for x in os.listdir(path) if   '~' not in x]
d = [pd.read_excel(os.path.join(path,i)) for i in l]
df1 = pd.concat(d)




c = df1['旁白'].dropna()
c[c.str.contains('事无')]


c = df1['玩家说话'].dropna()
c[c.str.contains('决对')]

c = df1['男主说话'].dropna()
c[c.str.contains('事无')]

#%%


#%%
