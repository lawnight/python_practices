# -*- coding: utf-8 -*-
import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}


def getInfo():
    try:
        url = r'http://stockpage.10jqka.com.cn/1A0001/quote/header/'
        context = requests.get(url,headers=headers)
        obj = json.loads(context.text)
        return obj['data']['1A0001']
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print(getInfo())