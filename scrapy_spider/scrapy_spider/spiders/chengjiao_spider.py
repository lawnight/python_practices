# -*- coding: UTF-8 -*-
import scrapy

from scrapy.selector import Selector
from scrapy.http import HtmlResponse


from scrapy.loader import ItemLoader
from scrapy_spider.items import *

import time


# 房管局成交信息，每天23:00 同步
# http://www.cdfgj.gov.cn/SCXX/Default.aspx


class chengjiaoSpider(scrapy.Spider):
    name = "chengjiao"
    content = ""

    custom_settings = {
        'SOME_SETTING': 'some value',
    }

    def start_requests(self):
        url = r'http://www.cdfgj.gov.cn/SCXX/Default.aspx'
        try:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request
        except Exception as e:
            print(e)

    def parse(self, response):

        # name = response.meta['name']
        # houseList = response.xpath("//div[@class='houseList']")
        item = ItemLoader(item=Chengjiao(), response=response)
        # 新房成交

        new_xpath = r'//*[@id="form1"]/div/table[3]/tr/td[2]/div/table[1]/tr[2]/td/table/tr[%d]/td[3]/text()'
        # r'//*[@id="form1"]/div/table[3]/tr/td[2]/div/table[1]/tbody/tr[2]/td/table/tbody/tr[4]/td[3]'

        item.add_xpath('n_jj', new_xpath % 3, re='[0-9]+')
        item.add_xpath('n_jn', new_xpath % 4, re='[0-9]+')
        item.add_xpath('n_ch', new_xpath % 5, re='[0-9]+')
        item.add_xpath('n_qy', new_xpath % 6, re='[0-9]+')
        item.add_xpath('n_wh', new_xpath % 7, re='[0-9]+')
        item.add_xpath('n_gx', new_xpath % 8, re='[0-9]+')

        # 二手房成交
        #//*[@id="form1"]/div/table[3]/tbody/tr/td[2]/div/table[2]/tbody/tr[2]/td/table/tbody/tr[3]/td[3]

        old_xpath = r'//*[@id="form1"]/div/table[3]/tr/td[2]/div/table[2]/tr[2]/td/table/tr[%d]/td[3]/text()'

        item.add_xpath('o_jj', old_xpath % 3, re='[0-9]+')
        item.add_xpath('o_jn', old_xpath % 4, re='[0-9]+')
        item.add_xpath('o_ch', old_xpath % 5, re='[0-9]+')
        item.add_xpath('o_qy', old_xpath % 6, re='[0-9]+')
        item.add_xpath('o_wh', old_xpath % 7, re='[0-9]+')
        item.add_xpath('o_gx', old_xpath % 8, re='[0-9]+')

        item.add_value('date',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )

        return item.load_item()
