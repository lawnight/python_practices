#%%
import pandas as pd
from tabula import read_pdf
d = read_pdf(r'd:\20200119105535_27522.pdf',pages='all')
df = pd.concat(d)
key1 = '申论\r成绩'
key2 = '行政职业能力测验\r成绩'
#%%
df['sum'] = df[key1] + df[key2]

df['a'] = pd.cut(df[key1],range(0,200,5),right=False)
df['b'] = pd.cut(df[key2],range(0,200,5),right=False)
df['c'] = pd.cut(df['sum'],range(0,200,5),right=False)

a_series = df.groupby('a').size()
b_series = df.groupby('b').size()
c_series = df.groupby('c').size()
# %%
c = pd.DataFrame([a_series,b_series],index=['a','b'])
c = c.loc[:, (c != 0).any(axis=0)]
c.plot(kind='bar',stacked=True)
#%%
c_series.plot(kind='pie',autopct='%1.1f%%')
# %%
