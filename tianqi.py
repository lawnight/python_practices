# -*- coding: UTF-8 -*-
import requests
import re
import json
from utils import *


def getInfo():
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

    # print(info)

    return info

getInfo()

