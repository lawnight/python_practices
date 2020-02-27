import sys
import os
import configparser
import hashlib
import json
import socket
import requests
import time

from jd_utils import logger

_dnscache = {}

def parse_json(s):
    begin = s.find('{')
    end = s.rfind('}') + 1
    return json.loads(s[begin:end])


def response_status(resp):
    if resp.status_code != requests.codes.OK:
        print('Status: %u, Url: %s' % (resp.status_code, resp.url))
        return False
    return True


def _setDNSCache():
    """
    Makes a cached version of socket._getaddrinfo to avoid subsequent DNS requests.
    """

    def _getaddrinfo(*args, **kwargs):
        global _dnscache
        if args in _dnscache:
            # print(str(args) + " in cache")
            return _dnscache[args]

        else:
            # print(str(args) + " not in cache")
            _dnscache[args] = socket._getaddrinfo(*args, **kwargs)
            return _dnscache[args]

    if not hasattr(socket, '_getaddrinfo'):
        socket._getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = _getaddrinfo

class Config(object):
    def __init__(self, config_file='configDemo.ini'):
        self._path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = configparser.ConfigParser() # 实例化ConfigParser类，_config有read/sections/options等方法
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8-sig')

    def get(self, section, name):
        return self._config.get(section, name)

    def getRaw(self, section, name):
        return self._configRaw.get(section, name)


def getconfig():
    config = Config()
    cookies_String = config.getRaw('config', 'cookies_String')
    mail = config.getRaw('config', 'mail')
    sc_key = config.getRaw('config', 'sc_key')
    messageType = config.getRaw('config', 'messageType')
    modelType = config.getRaw('V2', 'model')
    area = config.getRaw('config', 'area')
    skuidsString = config.getRaw('V2', 'skuids')
    skuids = str(skuidsString).split(',')
    # 验证码服务地址
    captchaUrl = config.getRaw('Temporary', 'captchaUrl')
    if not modelType:
        logger.error('请在configDemo.ini文件填写下单model')

    if len(skuids[0]) == 0:
        logger.error('请在configDemo.ini文件中输入你的商品id')
        sys.exit(1)

    eid = config.getRaw('Temporary', 'eid')
    fp = config.getRaw('Temporary', 'fp')
    payment_pwd = config.getRaw('config', 'payment_pwd')

    return cookies_String, mail, sc_key, messageType, modelType, area, skuidsString, skuids, captchaUrl, eid, fp, payment_pwd

def png2base64():
    import base64
    f = open('structure.png', 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    f.close()
    print(ls_f)

def good_stock(self, skuId, area_id):
    """
    监控库存
    :return:
    """
    url = "https://c0.3.cn/stocks"

    params = {
        "skuIds": skuId,
        "area": area_id,  # 收货地址id
        "type": "getstocks",
        "_": int(time.time() * 1000)
    }

    headers = {"Referer": f"https://item.jd.com/{skuId}.html",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/75.0.3770.142 Safari/537.36",
                }
    try:
        response = requests.get(url, params=params, headers=headers)
        print(response.text)    # 33: 现货    34: 无货     40: 可配货
        json_dict = json.loads(response.text)
        stock_state = json_dict[skuId]['StockState']
        stock_state_name = json_dict[skuId]['StockStateName']
        return stock_state, stock_state_name
    except Exception as e:
        print(e)

    return 0, ''
if __name__ == '__main__':
    #png2base64()
    skuids = 100011385146
    area = '2_2830_51800_0'
    print(good_stock(None,skuids,area))
