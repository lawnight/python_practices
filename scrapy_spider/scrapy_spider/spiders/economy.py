import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import re
from scrapy_spider.items import *


class economy(scrapy.Spider):
    name = "economy"
    content = ""

    start_urls = [r'http://gold.hexun.com/hjxh/']


    def parse(self, response):        
        gold = response.xpath('//*[@id="mainbox"]/div[2]/div[5]/table/tbody/tr[2]/td[2]/text()').get()        
        silver = response.xpath('//*[@id="mainbox"]/div[2]/div[5]/table/tbody/tr[3]/td[2]/text()').get()
        data =  {'gold':gold,'silver':silver}
        print(data)
        yield data
                

    