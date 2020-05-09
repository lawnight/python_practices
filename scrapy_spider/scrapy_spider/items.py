# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class House(scrapy.Item):
    # 小区名字
    name = scrapy.Field()
    # 建筑年代
    year = scrapy.Field()
    # 建筑位置
    location = scrapy.Field()
    # 物业公司
    wy = scrapy.Field()
    # 开发商
    kfs = scrapy.Field()
    # 房屋总数
    house_count = scrapy.Field()
    # 楼栋总数
    build_count = scrapy.Field()
    # 建筑类型
    build_type = scrapy.Field()
    # url
    url = scrapy.Field()
    # 二手成交数量
    cj_count = scrapy.Field()
    # 预估价格
    price = scrapy.Field()
    # coordinate
    coordinate = scrapy.Field()


class Chengjiao(scrapy.Item):
    n_jj = scrapy.Field()
    n_jn = scrapy.Field()
    n_ch = scrapy.Field()
    n_wh = scrapy.Field()
    n_qy = scrapy.Field()
    n_gx = scrapy.Field()

    o_jj = scrapy.Field()
    o_jn = scrapy.Field()
    o_ch = scrapy.Field()
    o_wh = scrapy.Field()
    o_qy = scrapy.Field()
    o_gx = scrapy.Field()

    date = scrapy.Field()


class Stock(scrapy.Item):
    value = scrapy.Field()


class HmateItem(scrapy.Item):
    image_names = scrapy.Field()
    floder = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()