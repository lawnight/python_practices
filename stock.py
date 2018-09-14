
import requests
import json


def getInfo():
    try:
        url = r'http://stockpage.10jqka.com.cn/1A0001/quote/header/'

        context = requests.get(url)

        obj = json.loads(context.text)

        return obj['data']['1A0001']
    except Exception as e:
        print(e)
