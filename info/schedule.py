# -*- coding: UTF-8 -*-
#定时抓取
import subprocess
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import logging
import funi
import analysis_csv
import news_scrapy
import utils

#抓取房管局的成交,成交不及时，只有住宅，透明网的数据更有参考性，暂时
def scrapy_chengjiao():
    print('scrapy_chengjiao')
    os.system('scrapy crawl chengjiao')

def scrapy_funi():
    print('scrapy_funi')
    funi.getInfo()

def analysis():
    analysis_csv.analysis()

def news():
    return news_scrapy.getInfo()


# 输出时间
def scrapy_job():
    #scrapy_funi()
    #analysis()
    info = news()
    utils.sendMail('我的资讯',info)

# BlockingScheduler
print('start run this script')
logging.basicConfig()
os.chdir('scrapy_spider')
scheduler = BlockingScheduler()

scheduler.add_job(scrapy_job, 'cron', day_of_week='0-6', hour=06, minute=10)

print('start scheduler')
scrapy_job()
scheduler.start()
# analysis_csv.analysis()
