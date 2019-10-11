# -*- coding: UTF-8 -*-
# 漫画抓取 ，requestheader中传入cookie 免除登陆  (资源已经被下架)
import json
import csv
import datetime
from utils import *
from lxml import etree
import requests
import random

# 一页内20话
urls = []
xpath = r'//*[@id="index_ajax_list"]'
url = 'http://www.xoiof.com/h-mate/page_3.html'
data = requests.get(url)
html = etree.HTML(data.text)
a = html.xpath(xpath)[0]
for ele in a.getchildren():
    urls.append(ele.getchildren()[0].attrib['href'])

# session = requests.Session()
# payload={'log':'lawnight',
# 'pwd':'jiangtao12'}
# session.post('http://www.xoiof.com/login', data=payload)

import browser_cookie3 
cj = browser_cookie3.load('www.xoiof.com')
cj2={'Hm_lvt_2731e0269cd08158974f8e0d8a366836':'1548289309','wordpress_test_cookie':'WP+Cookie+check', 'Hm_lpvt_2731e0269cd08158974f8e0d8a366836':'1548343294'
}


headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7,zh-TW;q=0.6',
'Cache-Control':'max-age=0',
'Cookie':'Hm_lvt_2731e0269cd08158974f8e0d8a366836=1548289309; wordpress_test_cookie=WP+Cookie+check; wordpress_logged_in_7a48bfd769b4b84cc8a8daf8e52cf825=lawnight%7C1548516118%7CUSTCMMgBtx1dhW3ZErzyfP3AzVu21WoYpHqKZC9kGQ5%7Cbd03f5568676230c276f1130d3c8bdc2c73b44edca3035b9d9bf1e01082bfa28; Hm_lpvt_2731e0269cd08158974f8e0d8a366836=1548344787',
'Host':'www.xoiof.com',
'Proxy-Connection':'keep-alive',
'Referer':'http://www.xoiof.com/h-xiaoyuan',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

}


def getImage(num,sNum,url):
    data = requests.get(url,cookies=cj,headers=headers).text
    html = etree.HTML(data)
    path = './manhua/{}'.format(num) 
    if not os.path.exists(path):
        os.mkdir(path)
    next = ''
    count = 1
    for i in html.xpath(r'//a'):
        if 'title' in i.attrib and '点击图片查看下一张' in i.attrib['title']:
            imgUrl = i.find('img').attrib['src']
            name = i.find('img').attrib['alt']
            name = name.replace('动漫美女邪恶漫画污到你湿！','')
            r = requests.get(imgUrl)
            with open('{}/{}_{} {}.png'.format(path,sNum,count,name), 'wb+') as f:
                print('保存{}...'.format(name))
                count = count+1
                f.write(r.content)
            n = i.attrib['href']
            if '_' in n:
                next = n
    if len(next)>1:
        getImage(num,sNum+1,next)
    pass

import threading
for i,url in enumerate(urls):
    idx = i+21
    if idx<=9:
        continue
    print(idx,url,"downing")
    
    t =threading.Thread(target=getImage,args=(idx,1,url))
    t.start()