# -*- coding: UTF-8 -*-
import utils
import csv
import os
from collections import deque
import tianqi
import stock


def sumCount(row):
    return int(row['1B']) + int(row['2B']) + int(row['3B']) + int(row['4B']) + int(row['5B'])
# https://tianqi.2345.com/t/map_js/china.js?_=1518315957850


def getWearth():
    info = tianqi.getInfo()
    return '天气:%s-%s %s转%s 风向:%s' % (
        info['minTem'], info['maxTem'],info['day'],info['night'],info['wind'])

def getStock():
    info = stock.getInfo()
    #  return '沪市:%s 变化:%s'%info[10],info['199112']
    if info:
        return '沪市:%s '%info['10']
    else:
        return ''
   

def analysis():

    with open('saleInfo.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        dqu = deque(reader, 2)

        if len(dqu) == 2:
            lastRow = dqu.pop()
            secondRow = dqu.pop()

            sale1 = sumCount(secondRow) - sumCount(lastRow)
            sale2 = int(secondRow['5B']) - int(lastRow['5B'])
            left = int(lastRow['5B'])

            more_sale = int(lastRow['totalAmount']) - \
                int(secondRow['totalAmount'])

            str1 = '蓝光昨天售出:%d 5号楼售出:%d 5号楼剩余:%d' % (sale1, sale2, left)
            
            str2 = '昨天成都总出售:%s 总成交:%s 环比前天出售:%d' % (
                lastRow['totalAmount'], lastRow['totalPrice'], more_sale)

            msg = '\n'.join([utils.getTime(), getWearth(),getStock(),str1, str2])

            utils.sendMail('我的资讯',msg )
