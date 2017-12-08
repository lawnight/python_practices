# -*- coding: utf-8 -*-
# 通过高德webapi，通过公交站的名字，取得公交站的信息（包括坐标），保存为csv
import requests
import pandas as pd
from pandas import DataFrame
import json
import time


url = r'http://restapi.amap.com/v3/place/text'

data_info = {}


def getBusInfo(name, count):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    # key=您的key&keywords=北京大学&types=高等院校&city=北京&children=1&offset=20&page=1&extensions=all
    params = {
        'key': '2b04492c318299271fc82b1afe10a2c9',
        'keywords': name,
        # 'types': '高等院校',
        'city': '成都',
        'children': 1,
        'offset': 20,
        'page': 1,
        'extensions': 'all',

    }
    response = requests.get(url, params=params)
    # print())
    content = response.content.decode('utf-8')

    # content = u'{"status":"1","count":"1","info":"OK","infocode":"10000","suggestion":{"keywords":[],"cities":[]},"pois":[{"id":"BV10327499","name":"龙腾中路龙欣路口站(公交站)","tag":[],"type":"交通设施服务;公交车站;公交车站相关","typecode":"150700","biz_type":[],"address":"70路;100路;165路","location":"104.016388,30.651901","tel":[],"postcode":[],"website":[],"email":[],"pcode":"510000","pname":"四川省","citycode":"028","cityname":"成都市","adcode":"510107","adname":"武侯区","importance":[],"shopid":[],"shopinfo":"2","poiweight":[],"gridcode":"4504708100","distance":[],"navi_poiid":[],"entr_location":[],"business_area":"双楠","exit_location":[],"match":"0","recommend":"0","timestamp":[],"alias":[],"indoor_map":"0","indoor_data":{"cpid":[],"floor":[],"truefloor":[],"cmsid":[]},"groupbuy_num":"0","discount_num":"0","biz_ext":{"rating":[],"cost":[]},"event":[],"children":[],"photos":[]}]}'

    jobject = json.loads(content)

    if jobject['status'] == '1':
        pois = jobject['pois']
        if len(pois) >= 1:
            info = pois[0]
            info['query_name'] = name
            info['line_count'] = count
            data_info[info['id']] = info
            print('succees:' + name)
        else:
            print('error:len:' + name)

# df = DataFrame(content,index=['bus_name','bus_type','bus_time','bus_cost','bus_company','bus_update','bus_length','line_x','sites_x_list','line_y','sites_y_list'])


# getBusInfo('龙腾中路龙欣路口站(公交站)')


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


if __name__ == '__main__':
    # get last station info
    t = pd.read_csv('bus_station_info.csv')
    queried_name = t['query_name'].values

    bus_serial = get_all_bus_station()
    bus_serial = bus_serial + "(公交站)"

    for name, count in bus_serial.value_counts().iteritems():
        try:
            if name in queried_name:
                pass
            else:
                getBusInfo(name, count)
        except Exception as ex:
            print(ex)
        time.sleep(1 / 20.0)

    df = DataFrame(data_info)
    df = df.T
    df.to_csv('bus_station_info.csv')
