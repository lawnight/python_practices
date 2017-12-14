# -*- coding: utf-8 -*-
# 过滤非法，取出需要的数据
from get_bus_station_info import get_all_bus_station
import pandas as pd
from pandas import DataFrame
import json

serials = get_all_bus_station()


t = pd.read_csv('bus_station_info.csv')

# 有公交站的location
correct_t = t[(t['pname'] == '四川省') & (t['typecode'] == '150700')]
correct_t = correct_t[['name', 'location', 'line_count']]

data = []
for columns, row in correct_t.iterrows():
    # print(columns)
    print(row)

    map = {}

    map['name'] = row['name']
    map['value'] = []
    obj = row['location'].split(',')
    map['value'].append(obj[0])
    map['value'].append(obj[1])

    map['value'].append(row['line_count'])

    # print(map)
    data.append(map)
    


with open('bus_station_location.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)
