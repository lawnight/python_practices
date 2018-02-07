# -*- coding: UTF-8 -*-
#定时抓取
import subprocess
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import logging
import funi
import analysis_csv

#抓取房管局的成交,成交不及时，只有住宅，透明网的数据更有参考性，暂时
def scrapy_chengjiao():
    print('scrapy_chengjiao')
    os.system('scrapy crawl chengjiao')

def scrapy_funi():
    print('scrapy_funi')
    funi.getInfo()

def analysis():
    analysis_csv.analysis()


# 输出时间
def scrapy_job():
    scrapy_funi()

    analysis()

# BlockingScheduler
print('start run this script')
logging.basicConfig()
os.chdir('scrapy_spider')
scheduler = BlockingScheduler()

scheduler.add_job(scrapy_job, 'cron', day_of_week='0-6', hour=23, minute=50)

print('start scheduler')
scheduler.start()
# analysis_csv.analysis()

