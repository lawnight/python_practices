# -*- coding: UTF-8 -*-
##蓝光每日成交抓取
#透明网的抓取，最先通过web网页，先通过burp suite来分析协议。需要在设置中开启对amf的支持。
#发现amf的交互，都做了加密。需要破解swf文件。难度大，
# 最后发现android手机直接用post请求获得信息，而且没有加密。得到post地址。
#透明网的抓取
import requests
import json
import csv
from utils import *



fileName = 'saleInfo.csv'

from collections import OrderedDict

request_info = OrderedDict([
     ('1B' , 'e1b28e3e-8d21-423c-9a52-db8bc42a95cf'),
    ('2B' , 'd4ebca50-0191-40e7-8ce1-3e7b72833e1a'),
    ('3B' , 'e09cf1f5-58df-42a8-8aba-0925d8ae5413'),
    ('4B' , 'd85e5e03-94d7-42bb-a685-3a52be7dd05d'),
    ('5B' , '190192e4-7734-44fd-8e53-cfd9e4bfe198')
    ])

careBuild = request_info.values()

data={'cityId':'1',
'tal':'ANDROID',
'tal_id' : '902558776994568',
'buildingIdArray' : ','.join(careBuild),
'communityId' : '13715'
}


def getValueByKey(key,buildList):
    for build in buildList:
        if build['buildingId']==key:
            return build['saleAmount']

def getInfo():
    context = requests.post('http://mobileapi.funi.com/m/community/buildingAmount.json',data=data)
    obj = json.loads(context.text)
    buildList = obj['data']
    info=OrderedDict()
    info['community'] = '蓝光T-Max'
    for key,value in request_info.items():
        value = getValueByKey(value,buildList)
        if value:
            info[key] = value
    #总成交数
    context = requests.get('http://mobileapi.funi.com/m/community/hotSale.json?tal_id=902558776994568&tal=ANDROID&cityId=1')
    obj = json.loads(context.content.decode('utf-8'))
    info['totalAmount'] = obj['data']['totalAmount']
    info['totalArea'] =  obj['data']['totalArea'].encode('utf-8')
    info['infoDate'] =  obj['data']['date'].encode('utf-8')
    info['totalPrice'] =  obj['data']['totalPrice'].encode('utf-8')
    info['date'] = getTime()
    writeCsv(fileName,info)









