#%%
import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import re


os.chdir('.')

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process = CrawlerProcess(get_project_settings())


### 执行指定spider
from scrapy_spider.spiders.economy import economy
process.crawl(economy)
process.start() 

# %%
