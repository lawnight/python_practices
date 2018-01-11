# -*- coding: UTF-8 -*-
import scrapy

from scrapy.selector import Selector
from scrapy.http import HtmlResponse


# 高新区领导信箱
# http://www.cdht.gov.cn/xinxiang/maillist.jspx?channelId=546&type=1,2,3
# http://www.cdht.gov.cn/xinxiang/maillist_2.jspx?channelId=546&type=1,2,3

#key_words = u"红树湾"
# u"关于中央第五环境保护督察组"
key_words = u"中和"


scrapy_url = 'http://www.cdht.gov.cn/xinxiang/maillist_%d.jspx?channelId=546&type=1,2,3'


class MaillistSpider(scrapy.Spider):
    name = "maillist"
    content = ""

    def start_requests(self):
        urls = [
            'http://www.cdht.gov.cn/xinxiang/maillist.jspx?channelId=546&type=1,2,3']

        for i in range(1, 30):
            str = scrapy_url % i
            urls.append(str)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        table = response.xpath("//li")
        findKey = key_words
        # findKey = ""
        ret = []

        for link in table:
            print '-' * 20
            if findKey in link.extract():
                url = link.xpath('span/a/@href').extract_first()
                url = "http://www.cdht.gov.cn/" + url
                yield scrapy.Request(url=url, callback=self.parse2)
        print '-' * 20

    def parse2(self, response):
        replace = "<font size='3' color='red'> %s </font>" % key_words


        content = response.selector.xpath("//div[contains(@class,'mt20 p20 gary_box')]").extract_first()
        local_content = content
   
        

        if key_words in local_content:
            
            if content:
                local_content = content.replace(key_words, replace)

            local_content = local_content + "<br><br>"
            self.content = self.content + local_content.encode('utf-8')

            # 待优化，不用每次保存
            filename = 'mail_out.html'
            with open(filename, 'wb') as f:
                f.write(self.content)
