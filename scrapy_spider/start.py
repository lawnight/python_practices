#%%
import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings

from scrapy_spider.spiders.economy import economy
from scrapy_spider.spiders.kanmanhua import kanmanhua






#%%
import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import re





### 执行指定spider
if __name__ == "__main__":
    os.chdir('.')
    process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
    process = CrawlerProcess(get_project_settings())

    process.crawl(kanmanhua)
    process.start() 

# %%
