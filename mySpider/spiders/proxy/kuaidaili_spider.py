import logging
import requests
import json

orderid = '908278477739119'  # 订单号

# 提取代理链接，以私密代理为例
api_url = "https://dps.kdlapi.com/api/getdps/?orderid={}&num=1&pt=1&dedup=1&format=json&sep=1"

logger = logging.getLogger(__name__)


def fetch_proxy():
    """
        提取代理
    """
    fetch_url = api_url.format(orderid)
    r = requests.get(fetch_url)
    if r.status_code != 200:
        logger.error("fail to fetch proxy")
        return False
    content = json.loads(r.content.decode('utf-8'))

    if content['data']:
        ips = content['data']['proxy_list']
    else:
        logger.error("fail to fetch proxy: %s" % content['msg'])
        ips = ''

    return ips
