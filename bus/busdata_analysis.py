import pandas as pd
import re

# pre post 先要预处理输出日志，才能读入table
# with open('Network_bus.txt') as f:
#     for line in f:
#         print(line)
#     with open('Network_bus2.txt','w+') as f2:
#         for line in f:
#             str = re.sub(regex,replaceMatch,line)
#             str = msg_regex.sub(replaceMatch2,str)
#             str = r'2017/'+str;
#             f2.write(str)
#             f2.flush


def convert_list(x):
    temp = eval(x)
    return temp

def get_all_bus_station():
    t = pd.read_csv('bus_info.csv')
    list_column = t['sites_x_list']
    new_column = list_column.map(convert_list)
    total_list = new_column.sum()
    total_series = pd.Series(total_list)
    return total_series

total_series = get_all_bus_station()

print (dir(total_series))