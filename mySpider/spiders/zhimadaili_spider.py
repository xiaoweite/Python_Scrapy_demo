import logging
import requests
import json
import redis
# from ..helper import Helper

# orderid = ''  # 暂无购买订单

# 提取代理链接，以私密代理为例
# api_url = "https://dps.kdlapi.com/api/getdps/?orderid=908278477739119&num=1&pt=1&dedup=1&format=json&sep=1"

# 提取独享IP
# 芝麻代理
#api_url = "http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=440000&city=440100&yys=0&port=1&pack=82738&ts=1&ys=1&cs=1&lb=1&sb=0&pb=45&mr=1&regions=&gm=4"
api_url = "http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&pack=82738&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions=&gm=4"
# 快代理
k_api_url = "https://dps.kdlapi.com/api/getdps/?orderid=908278477739119&num=1&pt=1&dedup=1&format=json&sep=1"

logger = logging.getLogger(__name__)


def zima_fetch_proxy():
    """
        提取代理
    """
    # fetch_url = api_url.format(orderid)
    r = requests.get(api_url)
    if r.status_code != 200:
        logger.error("fail to fetch proxy")
        return False
    content = json.loads(r.content.decode('utf-8'))

    if content['data']:
        ips = content['data']
    else:
        logger.error("fail to fetch proxy: %s" % content['msg'])
        ips = ''

    return ips

def kuai_fetch_proxy():
    """
        提取代理
    """
    # fetch_url = api_url.format(orderid)
    r = requests.get(k_api_url)
    if r.status_code != 200:
        logger.error("fail to fetch proxy")
        return False
    content = json.loads(r.content.decode('utf-8'))
    if content['data']['proxy_list']:
        ips = content['data']['proxy_list']
    else:
        logger.error("fail to fetch proxy: %s" % content['msg'])
        ips = ''

    return ips

if __name__ == '__main__':

    r = redis.Redis(host='120.78.164.142', port='6379', db=0,password='bu8515859', decode_responses=True)
    proxy_list = zima_fetch_proxy()
    proxy_ip_list = []
    for proxy in proxy_list:
        ip_prot = '{}:{}'.format(proxy['ip'], proxy['port'])
        #ip_prot = proxy
        proxy_ip_list.append(ip_prot)
    r.setex('proxy_ip_list', 600, ','.join(proxy_ip_list))

