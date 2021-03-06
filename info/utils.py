# -*- coding: UTF-8 -*-
import time
import os
import smtplib
import csv

from email.mime.text import MIMEText
from email.header import Header

def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def writeCsv(name,info):
    fieldnames = info.keys()
    need_header = True
    if  os.path.isfile(name):
        need_header = False
        
    with open(name, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if need_header:
            writer.writeheader()
        writer.writerow(info)

def sendMail(subject,msg):
    """ 发送邮件
    subject: 主题
    msg: 内容
    """
    message = MIMEText(msg, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)
    smtpObj.ehlo()
    smtpObj.login('nearisl@163.com', 'jiangtao12')
    print("msg",msg)
    smtpObj.sendmail('nearisl@163.com', 'nearisl@163.com',message.as_string())
    smtpObj.quit()



def convert2Map(text):
    '''
    把chrome拷贝下来的hearder字符串转换成map的形式，给requests使用
    '''
    header = {}
    for line in text.splitlines():
        if line:
            k,v = line.split(': ')
            header[k.strip()] = v.strip()
    return header

#sendMail('test','这是一封测试邮件2')