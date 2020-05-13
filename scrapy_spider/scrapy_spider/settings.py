# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy_spider'

SPIDER_MODULES = ['scrapy_spider.spiders']
NEWSPIDER_MODULE = 'scrapy_spider.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'scrapy_spider.pipelines.ImageNamePipeline': 1
   #'scrapy_spider.pipelines.economyPipeline': 2
}

# 下载图片的保存路径
IMAGES_STORE = r'D:\image'

# save info
info_path = r'e:\dailyGold.csv'