# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy.exporters import CsvItemExporter
import re
import os.path
import scrapy
from scrapy.pipelines.images import ImagesPipeline



class ImageNamePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # use 'accession' as name for the image when it's downloaded
        return [scrapy.Request(x, meta={'image_name': i,'floder':item['floder']}) for i,x in enumerate(item.get('image_urls', []))]

    # write in current folder using the name we chose before
    def file_path(self, request, response=None, info=None):
        return '/{}/{}.jpg'.format(request.meta['floder'],request.meta['image_name'])

class ScrapySpiderPipeline(object):
    def process_item(self, item, spider):
        return item



class CsvPipeline(object):
    def __init__(self):
        self.file = open("test11.csv", 'a+')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class stockPipeline(object):

    def open_spider(self, spider):
        file_name = "chengjiao.csv"
        self.file = open(file_name, 'a+')
        if spider.name == 'chengjiao':
            need_header = True
            if os.path.isfile(file_name):
                need_header = False

            if need_header:
                print('create chengjiao.csv header')
                header = 'n_jj,n_jn,n_ch,n_wh,n_qy,n_gx,o_jj,o_jn,o_ch,o_wh,o_qy,o_gx,date'
                self.file.writelines(header + '\n')

    def close_spider(self, spider):
        if self.file:
            self.file.flush()
            self.file.close()

    def process_item(self, item, spider):
        if spider.name == 'chengjiao':
            try:
                # print('+","+'.join(['item["%s"][0]'%i for i in array])) 通过这个临时程序生成下面的代码
                line = item["n_jj"][0] + "," + item["n_jn"][0] + "," + item["n_ch"][0] + "," + item["n_wh"][0] + "," + item["n_qy"][0] + "," + item["n_gx"][0] + "," + \
                    item["o_jj"][0] + "," + item["o_jn"][0] + "," + item["o_ch"][0] + "," + \
                    item["o_wh"][0] + "," + item["o_qy"][0] + "," + \
                    item["o_gx"][0] + "," + item["date"][0]
                self.file.writelines(line + '\n')
            except Exception as ex:
                print(ex)

            return item


class SelfCsvPipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        file_name = "chengjiao.csv"
        self.file = open(file_name, 'a+')
        if spider.name == 'chengjiao':
            need_header = True
            if os.path.isfile(file_name):
                need_header = False

            if need_header:
                print('create chengjiao.csv header')
                header = 'n_jj,n_jn,n_ch,n_wh,n_qy,n_gx,o_jj,o_jn,o_ch,o_wh,o_qy,o_gx,date'
                self.file.writelines(header + '\n')

    def close_spider(self, spider):
        if self.file:
            self.file.flush()
            self.file.close()

    def process_item(self, item, spider):
        if spider.name == 'chengjiao':
            try:
                # print('+","+'.join(['item["%s"][0]'%i for i in array])) 通过这个临时程序生成下面的代码
                line = item["n_jj"][0] + "," + item["n_jn"][0] + "," + item["n_ch"][0] + "," + item["n_wh"][0] + "," + item["n_qy"][0] + "," + item["n_gx"][0] + "," + \
                    item["o_jj"][0] + "," + item["o_jn"][0] + "," + item["o_ch"][0] + "," + \
                    item["o_wh"][0] + "," + item["o_qy"][0] + "," + \
                    item["o_gx"][0] + "," + item["date"][0]
                self.file.writelines(line + '\n')
            except Exception as ex:
                print(ex)

            return item

#for economy spider
import csv
import datetime


postData = {
  "appToken":"AT_8T4nKJGFO0ou8s13ZuEoDP6b8o6dPOkC",
  "content":"默认消息",
  "summary":"默认消息",
  "contentType":1,
  
  "uid":["UID_eIVknzhI7hBbIzCtHXkNsoRMFKHF"],
}

headers = {
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",   
   "Content-Type":"application/json",
   "Connection": "keep-alive",
}

# %%
import requests
def sendWeChart(title):
   sendMsg_url = 'http://wxpusher.zjiecode.com/api/send/message'
   postData['summary'] = title
   requests.get(sendMsg_url,headers=headers,params=postData)
   


class economyPipeline(object):
    
    header = ['date','gold','silver']
    filePath = r'e:\1.csv'    

    def open_spider(self, spider):
        print('open file',self.filePath)
        self.f = open(self.filePath,'a')        
    def process_item(self, item, spider):
        if spider.name == 'economy':
            try:
                print('economyPipeline',item)
                item['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')                
                self.f.write(','.join([item[x] for x in self.header])+'\n')
                sendWeChart("黄金{}，白银{} {}".format(item['gold'],item['silver'],item['date']))
            except Exception as ex:
                print(ex)
            return item
    def close_spider(self, spider):
        if self.f:
            self.f.flush()
            self.f.close()

