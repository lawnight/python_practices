# -*- coding: UTF-8 -*-
#定时抓取
import subprocess
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.twisted import TwistedScheduler
from datetime import datetime
import logging
import sys
# import scrapy_spider.start

import tools.logger as logger

log = logger.Logger('all.log',level='debug')



# BlockingScheduler

# 因为srapy的独特性，设置模块为里面的文件夹
sys.path.insert(0,os.path.join(os.path.abspath(os.path.dirname(__file__)),'scrapy_spider'))
print(sys.path)
os.chdir('scrapy_spider')
import scrapy_spider.start as start

# 定时任务
def scrapy_job():
    log.logger.info('run the job')
    start.start()

scheduler = TwistedScheduler()

scheduler.add_job(scrapy_job, 'cron', day_of_week='0-6', hour=18, minute=29)
scheduler.add_job(scrapy_job, 'cron', day_of_week='0-6', hour=9, minute=00)
scheduler.add_job(scrapy_job, 'cron', day_of_week='0-6', hour=14, minute=45)
scheduler.start()

log.logger.info('start')

from twisted.internet import reactor
reactor.run(installSignalHandlers = 0)


while(True):
    pass



