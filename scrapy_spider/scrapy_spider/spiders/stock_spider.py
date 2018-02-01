# -*- coding: UTF-8 -*-
import scrapy

from scrapy.selector import Selector
from scrapy.http import HtmlResponse


from scrapy.loader import ItemLoader
from scrapy_spider.items import *

import time


# 房管局成交信息，每天23:00 同步
# http://www.cdfgj.gov.cn/SCXX/Default.aspx


class stockSpider(scrapy.Spider):
    name = "stock"
    content = ""

    def start_requests(self):
        url = r'https://gupiao.baidu.com/stock/'
        try:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request
        except Exception as e:
            print(e)

    def parse(self, response):
        item = ItemLoader(item=Stock(), response=response)

        xpath = '//*[@id="app-wrap"]/div[2]/div/div[1]/strong/text()'
        item.add_xpath('value', xpath)
        return item.load_item()
