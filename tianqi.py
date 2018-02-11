# -*- coding: UTF-8 -*-
import requests


def getInfo():
    url =  r"https://tianqi.2345.com/t/map_js/china.js?_=1518315957850"
    context = requests.get(url)
    print context.text