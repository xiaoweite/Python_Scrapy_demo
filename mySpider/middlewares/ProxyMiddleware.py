import base64
import logging
from ..helper import Helper
from .. import settings

# 非开放代理且未添加白名单，需用户名密码认证
username = "gin.he"
password = "30tozlxe"

THRESHOLD = 3  # 换ip阈值
fail_time = 0  # 此ip异常次数


class ProxyMiddleware(object):
    def __init__(self):
        self.r = Helper.redis()
        using_proxy = self.r.get(settings.PROXY_IP_USING)
        self.proxy = using_proxy if using_proxy else Helper.proxy_ready(self.r)

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://{}'.format(self.proxy)  # 设置代理
        logging.info("using proxy: {}".format(request.meta['proxy']))
        print("使用的代理IP为：%s" % request.meta['proxy'])

    def process_response(self, request, response, spider):
        """
            如果状态码异常，则增加ip异常次数
            当异常次数达到阈值, 则更换ip,
            此换ip策略比较简略, 仅供参考
        """
        global fail_time, THRESHOLD
        if not(200 <= response.status < 300):
            fail_time += 1
            if fail_time >= THRESHOLD:
                logging.info("代理IP达到阈值: {}".format(self.proxy))
                Helper.update_proxy(self.r, self.proxy)
                fail_time = 0
        return response
