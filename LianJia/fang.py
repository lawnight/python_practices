# -*- coding: utf-8 -*-

# 成都小区的成交价

import requests
import random
from bs4 import BeautifulSoup
import re
import json

hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
       {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
       {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
       {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
       {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
       {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
       {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
       {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
       {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]


xiaoqu_list = []


def get_xiaoqu_info(url):
    try:
        chengjiao_url = url + "chengjiao/"

        chengjiao_url = 'http://changqiaojunlh.fang.com/chengjiao/'

        response = requests.get(
            url, headers=hds[random.randint(0, len(hds) - 1)])

        content = response.text

        soup = BeautifulSoup(content, "lxml")

       

        chengjiao_list = soup.find('tbody')



        print(chengjiao_list)
        
    except Exception as e:
        print (e)
        return

def page_spider(url):
    try:
        response = requests.get(
            url, headers=hds[random.randint(0, len(hds) - 1)])

        content = response.text

        soup = BeautifulSoup(content, "lxml")

        xiaoqu_list = soup.find('div', {'class': 'houseList'})

        # /html/body/div[4]/div[1]/ul
        for xq in xiaoqu_list:

            try:

                # print(xq)
                info_dict = {}

                name = xq.find('a', {'class', 'plotTit'})
                type = xq.find('span', {'class', 'plotFangType'})

                xiaoqu_url = xq.find('a', {'class', 'plotTit'})['href']
                xiaoqu_list.append(xiaoqu_url)
                get_xiaoqu_info(xiaoqu_url)

                print(xiaoqu_url)

                # info_dict.update({u'小区名称':xq.find('div',{'class':'title'}).text})

                # content=(xq.find('div',{'class':'info'}).text)
                # print(content)
                # info=re.match(r".+>(.+)</a>.+>(.+)</a>.+</span>(.+)<span>.+</span>(.+)",content)
                # if info:
                #     info=info.groups()
                #     info_dict.update({u'大区域':info[0]})
                #     info_dict.update({u'小区域':info[1]})
                #     info_dict.update({u'小区户型':info[2]})
                #     info_dict.update({u'建造时间':info[3][:4]})
                # command=gen_xiaoqu_insert_command(info_dict)
                # db_xq.execute(command,1)
            except Exception as e:
                print(e)
    except Exception as e:
        print (e)
        return


def xiaoqu_spider():
    url = r'http://esf.cd.fang.com/housing/'
    try:
        source_code = requests.get(
            url, headers=hds[random.randint(0, len(hds) - 1)])
        soup = BeautifulSoup(source_code.content, "lxml")
        # d = soup.find('div',{'class':'page-box house-lst-page-box'}).get('page-data')
        # obj = json.loads(d)
        # print(d)
        total_pages = 100
        # threads=[]
        for i in range(total_pages):
            url_page = r'http://esf.cd.fang.com/housing/__0_0_0_0_%d_0_0_0/' % (
                i + 1)
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


if __name__ == "__main__":
    xiaoqu_spider()
