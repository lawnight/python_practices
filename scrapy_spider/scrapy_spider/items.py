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
     # 小区名字
    name = scrapy.Field()
    # 成交总价格
    t_Price = scrapy.Field()
    # 成交单价
    a_price = scrapy.Field()
    # 成交时间
    date = scrapy.Field()
    # 成交面积
    area = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
