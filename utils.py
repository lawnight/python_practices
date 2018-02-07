# -*- coding: UTF-8 -*-
import time
import os
import smtplib

from email.mime.text import MIMEText
from email.header import Header

def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())



def sendMail(subject,msg):
    message = MIMEText(msg, 'plain', 'utf-8')
    # message['From'] = Header("菜鸟教程", 'utf-8')
    # message['To'] =  Header("测试", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')


    smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)
    smtpObj.ehlo()
    smtpObj.login('nearisl@163.com', 'jiangtao12')
    smtpObj.sendmail('nearisl@163.com', 'nearisl@163.com',message.as_string())
    smtpObj.quit()