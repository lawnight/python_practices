# -*- coding: utf-8 -*-
# 网上泄露的100w开房记录，存入mongodb，大概有1个G。
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import os
import csv

import re
from pymongo import MongoClient
from pymongo import WriteConcern
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne

client = MongoClient('mongodb://127.0.0.1:27017/')
collection = client.hotel.get_collection(
    'record', write_concern=WriteConcern(w=1, wtimeout=1))
import datetime

keys = ['陈尧', '吴哲文', '李江韬', '杨苗', '陈瑶','杨婷']

path = r'E:\hotel'
page = 1000
for item in os.listdir(path):
    csv_file = os.path.join(path, item)
    print('process', csv_file)
    # table = pd.read_csv(s)
    # for key in keys:
    #     temp = table[table.Name == key]
    #     print(temp)
    begin = datetime.datetime.now()
    # table =  pd.read_csv(csv_file,  skiprows=1000, chunksize=1)
    # print(table)
    # collection.bulk_write([InsertOne(row) for row in df])

    with open(csv_file, 'rU') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        bulk = []
        for row in csv_reader:
            bulk.append(row)
            if len(bulk) > 10000:              
                collection.bulk_write([InsertOne(row) for row in bulk])
                print('complete 1w')
                bulk = []

    end = datetime.datetime.now()
    print('cost:', (end - begin))
#     array = []
#     length = len(array)

#     for i in range(0,length,page):
#         reader = array[i:i+page]
#         collection.bulk_write([InsertOne(row) for row in reader])


# break

# table = pd.read_csv('1-200W.csv',nrows=2)
# print(table.columns)
# print(table.Name)
#
