import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import re

from scrapy_spider.items import *


class kanmanhua(scrapy.Spider):
    name = "kanmanhua"
    content = ""
    url = r'https://kanmanhuala.com'
    root_url = url+r'/book/4242'

    #https://kanmanhuala.com/chapter/32683
    def start_requests(self):
        
        yield scrapy.Request(url=self.root_url, callback=self.page_parse)

    def page_parse(self, response):
        for ele in response.xpath('//*[@id="detail-list-select"]').xpath('.//a'):
            url = ele.attrib['href']
            chapter = ele.xpath('text()').get() #这个api不方便
          
            new_url = self.url + url # >代表一页显示所有图片                 
            self.log('start process:'+new_url)
            yield scrapy.Request(new_url, self.section_parse,meta={'name':chapter})
            

    def section_parse(self, response):
        urls = response.xpath('//*[@id="content"]/div[2]/div').xpath('.//img/@data-original').getall() # 图片地址    
        if urls:
            return HmateItem(image_urls =urls ,image_names = list(range(1,len(urls))) ,floder = response.meta['name'] )