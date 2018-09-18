# -*- coding: UTF-8 -*-
##新闻的抓取
import requests
import json
import csv
import datetime
from utils import *
from bs4 import BeautifulSoup

baseUrl = r'http://paperpost.people.com.cn/all-rmrb-%02d-%02d-%02d.html'
def getInfo():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    url = baseUrl % (year,month,day)
   
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'lxml')

    result = soup.find('div').get_text()
    return result