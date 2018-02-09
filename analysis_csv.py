# -*- coding: UTF-8 -*-
import utils
import csv
import os
from collections import deque


def sumCount(row):
    return int(row['1B']) + int(row['2B']) + int(row['3B']) + int(row['4B']) + int(row['5B'])


def analysis():

    with open('saleInfo.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        dqu = deque(reader, 2)

        if len(dqu) == 2:
            lastRow = dqu.pop()
            secondRow = dqu.pop()

            sale1 =  sumCount(secondRow) - sumCount(lastRow)
            sale2 =  int(secondRow['5B']) - int(lastRow['5B']) 
            left = int(lastRow['5B'])

            more_sale = int(lastRow['totalAmount']) - \
                int(secondRow['totalAmount'])

            str1 = '蓝光昨天售出:%d 5号楼售出:%d 5号楼剩余:%d' % (sale1, sale2, left)
            str2 = '昨天成都总出售:%s 总成交:%s 比前天多出售:%d' % (
                lastRow['totalAmount'], lastRow['totalPrice'], more_sale)

            utils.sendMail('我的资讯', utils.getTime() + '\n' + str1 + '\n' + str2)

