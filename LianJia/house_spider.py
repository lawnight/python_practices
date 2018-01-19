# -*- coding: utf-8 -*-

import requests
import random
from bs4 import BeautifulSoup
import re
import json

hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]


def xiaoqu_chengjiao_spider(db_cj,xq_name=u"冠庭园"):
    """
    爬取小区成交记录
    """
    url=u"http://cd.lianjia.com/chengjiao/rs"+urllib2.quote(xq_name)+"/"
    try:
        req = urllib2.Request(url,headers=hds[random.randint(0,len(hds)-1)])
        source_code = urllib2.urlopen(req,timeout=10).read()
        plain_text=unicode(source_code)#,errors='ignore')   
        soup = BeautifulSoup(plain_text)
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        exception_write('xiaoqu_chengjiao_spider',xq_name)
        return
    except Exception,e:
        print e
        exception_write('xiaoqu_chengjiao_spider',xq_name)
        return
    content=soup.find('div',{'class':'page-box house-lst-page-box'})
    total_pages=0
    if content:
        d="d="+content.get('page-data')
        exec(d)
        total_pages=d['totalPage']
    
    threads=[]
    for i in range(total_pages):
        url_page=u"http://bj.lianjia.com/chengjiao/pg%drs%s/" % (i+1,urllib2.quote(xq_name))
        t=threading.Thread(target=chengjiao_spider,args=(db_cj,url_page))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def page_spider(url):
    try:
        response = requests.get(url,headers=hds[random.randint(0,len(hds)-1)])     
        content = response.content.decode('utf-8')  
        soup = BeautifulSoup(content,"lxml")  
    
        xiaoqu_list=soup.find('ul',{'class':'listContent'})
        print(type(xiaoqu_list))
        
        # /html/body/div[4]/div[1]/ul
        for xq in xiaoqu_list:
            print(xq)
            info_dict={}
            info_dict.update({u'小区名称':xq.find('div',{'class':'title'}).text})

            content=(xq.find('div',{'class':'info'}).text)
            print(content)
            info=re.match(r".+>(.+)</a>.+>(.+)</a>.+</span>(.+)<span>.+</span>(.+)",content)
            if info:
                info=info.groups()
                info_dict.update({u'大区域':info[0]})
                info_dict.update({u'小区域':info[1]})
                info_dict.update({u'小区户型':info[2]})
                info_dict.update({u'建造时间':info[3][:4]})
            # command=gen_xiaoqu_insert_command(info_dict)
            # db_xq.execute(command,1)
    except Exception as e:
        print (e)
        return
    

def xiaoqu_spider():
    url = r'https://cd.lianjia.com/xiaoqu/rs/'
    try:
        source_code = requests.get(url,headers=hds[random.randint(0,len(hds)-1)])
        # req = urllib2.Request()
        # source_code = urllib2.urlopen(req,timeout=5).read()
        #plain_text=unicode(source_code)#,errors='ignore')   
        soup = BeautifulSoup(source_code.content,"lxml")
   
        d = soup.find('div',{'class':'page-box house-lst-page-box'}).get('page-data')
        
        obj = json.loads(d)
        # exec(d)
        
        print(d)

        total_pages=obj['totalPage']
        
        # threads=[]
        for i in range(total_pages):
            url_page=u"http://cd.lianjia.com/xiaoqu/pg%d/" % (i+1)
            # t=threading.Thread(target=xiaoqu_spider,args=(db_xq,url_page))
            # threads.append(t)
            page_spider(url_page)
        # for t in threads:
        #     t.start()
        # for t in threads:
        #     t.join()
        # print (u"爬下了 %s 区全部的小区信息" % region)
    except Exception as e:
        print (e)
        return


if __name__=="__main__":
    # command="create table if not exists xiaoqu (name TEXT primary key UNIQUE, regionb TEXT, regions TEXT, style TEXT, year TEXT)"
    # db_xq=SQLiteWraper('lianjia-xq.db',command)
    
    # command="create table if not exists chengjiao (href TEXT primary key UNIQUE, name TEXT, style TEXT, area TEXT, orientation TEXT, floor TEXT, year TEXT, sign_time TEXT, unit_price TEXT, total_price TEXT,fangchan_class TEXT, school TEXT, subway TEXT)"
    # db_cj=SQLiteWraper('lianjia-cj.db',command)
    
    # #爬下所有的小区信息
    # for region in regions:
    #     do_xiaoqu_spider(db_xq,region)
    
    # #爬下所有小区里的成交信息
    # do_xiaoqu_chengjiao_spider(db_xq,db_cj)
    
    # #重新爬取爬取异常的链接
    # exception_spider(db_cj)
    xiaoqu_spider()
