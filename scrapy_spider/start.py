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

# scrapy shell http  来模拟
# response get 和 extract_first 一样


       
       

# The Images Pipeline has a few extra functions for processing images:
# Avoid re-downloading media that was downloaded recently
# Convert all downloaded images to a common format (JPG) and mode (RGB)
# Thumbnail generation
# Check images width/height to make sure they meet a minimum constraint

### 执行指定spider
process.crawl(hmate)
process.start() 