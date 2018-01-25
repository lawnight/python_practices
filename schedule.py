#定时抓取
import subprocess
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def scrapy_some():
    os.chdir('scrapy_spider')
    subprocess.Popen('scrapy crawl chengjiao')

# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    scrapy_some()

# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='0-6', hour=23, minute=50)
# scheduler.add_job(job, 'cron', day_of_week='0-6', hour=20, minute=42)
scheduler.start()