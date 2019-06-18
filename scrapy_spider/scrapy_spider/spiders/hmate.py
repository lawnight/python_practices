import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import re

from scrapy_spider.items import *


class hmate(scrapy.Spider):
    name = "hmate"
    content = ""

    root_url = r'https://mangapark.net/manga/h-mate'
    def start_requests(self):
        
        yield scrapy.Request(url=self.root_url, callback=self.page_parse)

    def page_parse(self, response):
        xpath = r'//*[@id="stream_6"]/div[2]/ul'

        for ele in response.xpath(xpath).xpath('.//a[@class="ml-1 visited ch"]'):
            url = ele.attrib['href']
            chapter = ele.xpath('text()').get() #这个api不方便
          
            new_url = self.root_url + url + ">" # >代表一页显示所有图片                 
            self.log('start process:'+new_url)
            return scrapy.Request(new_url, self.section_parse,meta={'name':chapter})
            

    def section_parse(self, response):
        d = response.body_as_unicode()
        d = [x for x in d.splitlines() if '_load_pages' in x]    
        if d:
            result = re.findall('(http.*?)"',d[0])
            if result: 
                urls = [x.replace('\\','') for x in result]
                return HmateItem(image_urls =urls ,image_names = list(range(1,len(urls))) ,floder = response.meta['name'] )
                # return {'file_urls':[x.replace('\\','') for x in result]}