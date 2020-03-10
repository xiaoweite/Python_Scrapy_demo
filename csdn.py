# -*- coding:utf-8 -*-

import requests

import random

import time

import re

user_agent_list=[
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
]

count=0

def Get_proxy_ip():
    headers = {
    #'Host': "www.xicidaili.com",
    'Host': "www.kuaidaili.com",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
    }
    req=requests.get(r'https://www.kuaidaili.com/free/inha/16/',headers=headers)
    html=req.text
    proxy_list=[]
    IP_list=re.findall(r'\d+\.\d+\.\d+\.\d+',html)
    port_lits=re.findall(r'<td data-title="PORT">\d+</td>',html)

    for i in range(len(IP_list)):
        ip=IP_list[i]
        port=re.sub(r'<td data-title="PORT">|</td>','',port_lits[i])
        proxy='%s:%s' %(ip,port)
        proxy_list.append(proxy)
    return proxy_list

def Proxy_read(proxy_list,user_agent_list,i):
    proxy_ip=proxy_list[i]
    print ('当前代理ip：%s'%proxy_ip)
    user_agent = random.choice(user_agent_list)
    print('当前代理user_agent：%s'%user_agent)
    sleep_time = random.randint(1,5)
    print('等待时间：%s s' %sleep_time)
    time.sleep(sleep_time)
    print('开始获取')
    headers = {
        'User-Agent': user_agent
    }

    proxies={
        'http': proxy_ip
    }

    # url='https://www.amazon.com/product-reviews/B07RGDZ1H4?sortBy=recent&filterByStar=three_star' #blog 地址
    url = 'http://www.itcast.cn/channel/teacher.shtml'  # blog 地址

    try:
        req = requests.get(url, headers=headers,  timeout=6,verify=False)
        html=req.text
        print (html)
    except Exception as e:
        print(e)
        print('******打开失败！******')
    else:
        global count
        count += 1
        print('OK!总计成功%s次！' % count)

if __name__ == '__main__':

    proxy_list = Get_proxy_ip()

    for i in range(100):

        Proxy_read(proxy_list, user_agent_list, i)
