#%%
import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings

from scrapy_spider.spiders.economy import economy




def start():

   
    runner = CrawlerRunner(get_project_settings())
    deferred = runner.crawl(economy)


