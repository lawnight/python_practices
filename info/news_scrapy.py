# -*- coding: UTF-8 -*-
##新闻的抓取
import requests
import json
import csv
import datetime
#from utils import *
from lxml import etree


baseUrl = r'http://paperpost.people.com.cn/all-rmrb-%02d-%02d-%02d.html'
def getInfo():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    url = baseUrl % (year,month,day)


    xpath = '/html/body/div[1]/div/div[1]/div[7]/div'
    
   
    data = requests.get(url)
    html = etree.HTML(data.text)
    root = html.xpath(xpath)    
    return root



print(getInfo())