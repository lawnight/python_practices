import requests
import pandas as pd
from pandas import DataFrame
import json
import time
import os


# 百度 web api，可以用来作为通用function
def getInfo_baidu(name):
    try:
        url = r'http://api.map.baidu.com/place/v2/search'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        # key=您的key&keywords=北京大学&types=高等院校&city=北京&children=1&offset=20&page=1&extensions=all
        params = {
            'ak': 'BSfi7kpeAhlvGr6NavgQlfRlr2jG4o26',
            'query': name,
            'region': '成都',
            'output': 'json',
            'tag': '房地产;住宅区',
            'scope': 2,
        }
        response = requests.get(url, params=params)
        content = response.content.decode('utf-8')
        # print(content)
        jobject = json.loads(content)
        status = jobject['status']
        if status == 0:
            pois = jobject['results']
            if len(pois) >= 1:
                return pois
            else:
                print('error:len:' + name)
        else:
            print('the error status:' + str(status) +
                  'the message is:' + jobject['message'])
    except Exception as ex:
        print(ex)


data_info = {}
new_save_file = 'new_save.csv'


if __name__ == '__main__':
    # get last station info
    t = pd.read_csv('xiaoqu_info.csv')

    print(len(t['name']))
    for name in t['name']:
        try:
            item = getInfo_baidu(name)
            time.sleep(1 / 20.0)
            if item:
                info = item[0]
                data_info[name] = info
        except Exception as ex:
            print(ex)

    df = DataFrame(data_info)
    df = df.T
    df.to_csv(new_save_file)
    print('finish crapy info')
