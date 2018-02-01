# -*- coding: utf-8 -*-
#利用python进行数据分析-将服务器的日志分析成table，然后进行分析,排序除打印最多的日志，然后进行定位分析
#%%
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import os

import re
# %matplotlib inline
# https://stackoverflow.com/questions/41898485/pandas-dataframe-error-matplotlib-axes-subplots-axessubplot

os.chdir(r'G:')

# regex = re.compile(r'\[([^\[\]]+)\]')

def replaceMatch(str):   
    return str.group(0).replace(' ','_')

def replaceMatch2(str):   
    return ' - ' + str.group(1).replace(' ','_')

regex = re.compile(r'\[.*?\]')
msg_regex = re.compile(r' - (.*)')
# test regex -----------------------------
# line = '11/09 17:32:36.218 DEBUG [Actor:Dispatcher-2] (NLoginImpl.java:152) - [debug] => [trace] enter req_login'
# print regex.findall(line)
# str = re.sub(regex,replaceMatch,line)
# print str




# pre post 先要预处理输出日志，才能读入table
# with open('out.txt') as f:
#     with open('out2.txt','w+') as f2:
#         for line in f:
#             str = re.sub(regex,replaceMatch,line)
#             str = msg_regex.sub(replaceMatch2,str)
#             str = r'2017/'+str;
#             f2.write(str)
#             f2.flush

table = pd.read_table('out2.txt',sep='\s+',error_bad_lines=False,skiprows={0},names=['date','time','level','thread','file','sep','msg'],nrows=1000)
table['file'].fillna('Missing')
table['t'] = table['date'] + " " + table['time']

#set index
t2 = table.set_index('t')
t2.index = pd.to_datetime(t2.index,format=r'%Y/%m/%d %H:%M:%S.%f',errors = 'coerce')

vc = table['file'].value_counts()
vc[:10].plot(kind='barh',rot=0)
plt.show()

# os.chdir(r'/Users/near/code/python')
