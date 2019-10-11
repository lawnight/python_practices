# -*- coding: UTF-8 -*-
# 链接失效 
import scrapy

from scrapy.selector import Selector
from scrapy.http import HtmlResponse


# 高新区领导信箱
# http://www.cdht.gov.cn/xinxiang/maillist.jspx?channelId=546&type=1,2,3
# http://www.cdht.gov.cn/xinxiang/maillist_2.jspx?channelId=546&type=1,2,3

#key_words = u"红树湾"
# u"关于中央第五环境保护督察组"
key_words = u"中和"
scrapy_url = 'http://www.cdht.gov.cn/zwgktzgg/index_%d.jhtml'

class NoticeSpider(scrapy.Spider):
    name = "notice"
    content = ""

    def start_requests(self):
        urls = ['http://www.cdht.gov.cn/zwgktzgg/index.jhtml']

        for i in range(1, 30):
            str = scrapy_url % i
            urls.append(str)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        table = response.xpath("//tr")
        findKey = key_words
        # findKey = ""
        ret = []

        for link in table:
            # print '-' * 20
                        #print("process link:%s" % link.extract())
            if findKey in link.extract():
                url = link.xpath('td/a/@href').extract_first()
                print(type(url))
                yield scrapy.Request(url=url, callback=self.parse2)
        # print '-' * 20
                print('processed page')

    def parse2(self, response):
        replace = "<font size='3' color='red'> %s </font>" % key_words
        local_content = (response.selector.xpath(
            "//div[contains(@class,'p20 gary_bg3')]").extract_first()).replace(key_words, replace)

        if key_words in local_content:
            self.content = self.content + local_content.encode('utf-8')

            # 待优化，不用每次保存
            filename = 'notice_out.html'
            with open(filename, 'wb') as f:
                f.write(self.content)
