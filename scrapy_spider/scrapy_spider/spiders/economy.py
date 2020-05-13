import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import re



class economy(scrapy.Spider):
    name = "economy"
    content = ""
    # start_urls = [r'http://gold.hexun.com/hjxh/'] 这个页面稳定
    start_urls = [r'https://www.spdrgoldshares.com/ajax/home/']
   

    def parse(self, response):        
        gold = response.xpath('ajaxUSD/text()').get()
        # silver = response.xpath('//*[@id="mainbox"]/div[2]/div[5]/table/tbody/tr[3]/td[2]/text()').get()
        # open_gold = response.xpath('//*[@id="mainbox"]/div[2]/div[5]/table/tbody/tr[3]/td[5]/text()').get()
        data =  {'gold':gold,'silver':0}
        print(data)
        yield data
    