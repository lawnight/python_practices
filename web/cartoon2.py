# -*- coding: UTF-8 -*-
import json
import csv
import datetime
from lxml import etree
import requests
import random
import re
import logging

# 每话 url
entry = r'https://mangapark.net/manga/h-mate'
urls = [] 

def mainPage():
    xpath = r'//*[@id="stream_6"]/div[2]/ul'
    logging.info('mainPage')
    data = requests.get(entry)
    html = etree.HTML(data.text)
    a = html.xpath(xpath)[0]
    for elm in a.findall('li'):
        url = elm.find('.//a[@class="ml-1 visited ch"]')
        url = url.attrib['href']
        urls.append(url)
        logging.info(url)
    
    
# get_section(section_url)

def get_section(url):
    """
    :param url:话第一页的地址
    """
    section_img = []
    for i in range(1,20):
        new_url = url[0:-1] + str(i)
        print('start process',new_url)
        data = requests.get(new_url,timeout = 10)
        if data.status_code != 200:
            break
        d = data.text
        d = [x for x in d.splitlines() if '_load_pages' in x]    
        if d:
            result = re.findall('http.*?"',d[0])
            if result:
                section_img.append(result[0])
        else:
            break
    return section_img


if __name__ == '__main__':
    logging.basicConfig(
        filename='app.log',
        level = logging.INFO,
        format = '%(asctime)s %(levelname)s %(message)s'
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    
    logging.info('start')
    mainPage()