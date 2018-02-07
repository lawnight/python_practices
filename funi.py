# -*- coding: UTF-8 -*-
import requests
import json
import csv
from utils import *

fileName = 'saleInfo.csv'

from collections import OrderedDict

request_info = OrderedDict([
     ('1号楼' , 'e1b28e3e-8d21-423c-9a52-db8bc42a95cf'),
    ('2号楼' , 'd4ebca50-0191-40e7-8ce1-3e7b72833e1a'),
    ('3号楼' , 'e09cf1f5-58df-42a8-8aba-0925d8ae5413'),
    ('4号楼' , 'd85e5e03-94d7-42bb-a685-3a52be7dd05d'),
    ('5号楼' , '190192e4-7734-44fd-8e53-cfd9e4bfe198')
    ])


careBuild = request_info.values()

data={'cityId':'1',
'tal':'ANDROID',
'tal_id' : '902558776994568',
'buildingIdArray' : ','.join(careBuild),
'communityId' : '13715'}



def getValueByKey(key,buildList):
    for build in buildList:
        if build['buildingId']==key:
            return build['saleAmount']



def writeCsv(name,info):
    fieldnames = info.keys()
    
    need_header = True
    if  os.path.isfile(name):
        need_header = False
        
    with open(name, 'ab') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if need_header:
            writer.writeheader()
        writer.writerow(info)





def getInfo():
        
    context = requests.post('http://mobileapi.funi.com/m/community/buildingAmount.json',data=data)
    obj = json.loads(context.text)
    buildList = obj['data']

    info=OrderedDict()
    info['小区'] = '蓝光T-Max'
    for key,value in request_info.items():
        value = getValueByKey(value,buildList)
        if value:
            info[key] = value
    info['时间'] = getTime()
   

    writeCsv(fileName,info)









