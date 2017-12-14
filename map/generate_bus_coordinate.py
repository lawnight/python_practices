# -*- coding: utf-8 -*-
# 过滤非法，取出需要的数据
from get_bus_station_info import get_all_bus_station
import pandas as pd
from pandas import DataFrame
import json

serials = get_all_bus_station()


t = pd.read_csv('bus_station_info2.csv')

# 有公交站的location
# correct_t = t[(t['pname'] == '四川省') & (t['typecode'] == '150700')]

# 百度返回的信息很少，不能过滤
correct_t = t
correct_t = correct_t[['name', 'location', 'line_count']]

data = []
for columns, row in correct_t.iterrows():
    # print(columns)
    # print(row)

    map = {}

    map['name'] = row['name']
    map['value'] = []
    # 高德
    # obj = row['location'].split(',')
    # map['value'].append(obj[0])
    # map['value'].append(obj[1])

    obj = json.loads(row['location'].replace(r"'",r'"'))
    map['value'].append(obj['lng'])
    map['value'].append(obj['lat'])
   

    map['value'].append(row['line_count'])

    # print(map)
    data.append(map)


with open('bus_station_location.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)

print('done')
