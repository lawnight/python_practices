# -*- coding: UTF-8 -*-
# %%
import requests
import re
import json
from utils import *
from lxml import etree


def getWeather():
    url = r"https://tianqi.2345.com/t/map_js/china.js?_=1518315957850"
    context = requests.get(url)
    content = context.content.decode('utf-8')
    content = re.findall('{.*}', content)[0]
    obj = json.loads(content)

    info = {}

    info['name'] = obj["56294"]["name"].encode('utf-8')
    info['maxTem'] = obj["56294"]["maxTem"].encode('utf-8')
    info['minTem'] = obj["56294"]["minTem"].encode('utf-8')
    info['wind'] = obj["56294"]["wind"].encode('utf-8')

    info['day'] = obj["56294"]["day"].encode('utf-8')
    info['night'] = obj["56294"]["night"].encode('utf-8')

    # print(info)

    return info


def getGlod():
    url = r'http://gold.hexun.com/hjxh/'
    c = requests.get(url)
    html = etree.HTML(c.text)
    d = html.xpath('//*[@id="mainbox"]/div[2]/div[5]/table/tbody/tr[3]/td[2]')
    return d[0].text



if __name__ == '__main__':
    print(getGlod())

# %%
