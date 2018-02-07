# -*- coding: UTF-8 -*-
#定时抓取
import subprocess
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import logging
import funi

#抓取房管局的成交
def scrapy_chengjiao():
    print('scrapy_chengjiao')
    os.system('scrapy crawl chengjiao')

def scrapy_funi():
    print('scrapy_funi')
    funi.getInfo()

def analysis():
    pass


# 输出时间
def scrapy_job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    scrapy_chengjiao()
    scrapy_funi()

    analysis()

# BlockingScheduler
print('start run this script')
logging.basicConfig()
os.chdir('scrapy_spider')
scheduler = BlockingScheduler()

scheduler.add_job(scrapy_job, 'cron', day_of_week='0-6', hour=23, minute=50)



print('start scheduler')
# scheduler.start()
scrapy_funi()
