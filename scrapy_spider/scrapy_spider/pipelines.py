# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy.exporters import CsvItemExporter
import re
import os.path


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
