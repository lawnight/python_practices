# -*- coding: UTF-8 -*-
import scrapy

from scrapy.selector import Selector
from scrapy.http import HtmlResponse


from scrapy.loader import ItemLoader
from scrapy_spider.items import *


def get_xiaoqu_info(url):
    try:
        chengjiao_url = url + "chengjiao/"

    except Exception as e:
        print (e)
        return


class HouseSpider(scrapy.Spider):
    name = "house"
    content = ""

    def start_requests(self):
        total_pages = 100
        urls = []

        # threads=[]
        for i in range(total_pages):
            url_page = r'http://esf.cd.fang.com/housing/__0_0_0_0_%d_0_0_0/' % (
                i + 1)

            urls.append(url_page)

        for url in urls:
            try:
                request = scrapy.Request(url=url, callback=self.page_parse)
                yield request
            except Exception as e:
                print(e)

    def page_parse(self, response):
        # name = response.meta['name']
        # houseList = response.xpath("//div[@class='houseList']")
        xiaoqu_urls = response.xpath("//a[@class='plotTit']/@href")

        chengjiao_list = []
        house_list = []

        for xq in xiaoqu_urls:
            try:
                chengjiao_list.append(xq.extract() + "chengjiao/")
                house_list.append(xq.extract())
            except Exception as e:
                print(e)

        for url in house_list:
            request = scrapy.Request(url=url, callback=self.xiaoqu_parse)
            yield request

        # for url in chengjiao_list:
        #     request = scrapy.Request(url=url, callback=self.chengjiao_parse)
        #     request.meta['name'] = name
        #     yield request

    def xiaoqu_parse(self, response):
        print("start xiaoqu_parse")
        chengjiao_count = response.xpath(
            '//*[@id="xqwxqy_C01_16"]/a[2]/div/p[2]/text()').extract_first()

        length = len(response.xpath(
            '//div[@class = "Rinfolist"]/ul/li[not (@class="zygwbox")]'))
        
        if length == 7:
            item = ItemLoader(item=House(), response=response)
            item.add_xpath(
                'year', '//div[@class = "Rinfolist"]/ul/li[not (@class="zygwbox")][1]/text()')
            item.add_xpath(
                'build_type', '//div[@class = "Rinfolist"]/ul/li[not (@class="zygwbox")][2]/text()')
            item.add_xpath(
                'house_count', '//div[@class = "Rinfolist"]/ul/li[not (@class="zygwbox")][3]/text()')
            item.add_xpath(
                'location', '//div[@class = "Rinfolist"]/ul/li[not (@class="zygwbox")][4]/text()')
            item.add_xpath(
                'build_count', '//div[@class = "Rinfolist"]/ul/li[not (@class="zygwbox")][5]/text()')
            item.add_xpath(
                'wy', '//div[@class = "Rinfolist"]/ul/li[not (@class="zygwbox")][6]/text()')
            item.add_xpath(
                'kfs', '//div[@class = "Rinfolist"]/ul/li[not (@class="zygwbox")][7]/text()')
                
            item.add_xpath(
                'price', '//div[@class="Rbiginfo"]/span[1]/text()')

            item.add_xpath(
                'name', '//div[@class="Rbigbt clearfix"]/h1/strong/text()')

            item.add_value(
                'cj_count', chengjiao_count)

            item.add_value('url', response.url)
            print("return xiaoqu_parse")
            return item.load_item()
        else:
            print("xiaoqu info length less 7")

    # 成交信息的抓取
    def chengjiao_parse(self, response):
        name = response.meta['name']

        total_str = response.xpath(
            "//span[@class='red']/text()").extract_first()
        total = int(total_str)
        print(response.url + total_str)

        # 成交大于0，算出近10条的平均价格
        sample_count = 5

        if total > 0:
            print("chengjiao more than 0")
            tbody = response.xpath("//tbody")
            trList = tbody.xpath('.//tr')
            # print(type(tr))
            total_area = 0
            total_price = 0
            count = sample_count
            for inside_tr in trList:
                # print(type(inside_tr))
                area = inside_tr.xpath("./td[2]").re("[0-9]+")
                date = inside_tr.xpath("./td[3]").extract_first()
                t_price = inside_tr.xpath("./td[4]").re("[0-9]+")
                price = inside_tr.xpath("./td[5]").re("[0-9]+")

                if area:
                    area = area[0]
                    price = price[0]
                    # total_area = total_area + int(area)
                    # print("price:" + price)
                    # total_price = total_price + int(price)

                    count = count - 1
                    if count <= 0:
                        # 得到前几次的平均成交价
                        averge_price = total_price / sample_count
                        print("averge_price" + str(averge_price))
                        # house = House(name = 'test',price = averge_price)
                        item = ItemLoader(item=Chengjiao(), response=response)
                        item.add_value('a_price', price)
                        item.add_value('area', area)
                        item.add_value('t_price', t_price)
                        item.add_value('date', date)
                        item.add_value('name', name)
                        return item.load_item()
