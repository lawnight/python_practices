# 过滤非法，取出需要的数据
from get_bus_station_info import get_all_bus_station
import pandas as pd
from pandas import DataFrame

serials = get_all_bus_station()


t = pd.read_csv('bus_station_info.csv')

# 有公交站的location
correct_t = t[(t['pname'] == '四川省') & (t['typecode'] == '150700')]
print(correct_t[['name','location','line_count']])