import datetime

import re
import pytz
import json
import redis
import random

from math import ceil
from random import Random

from . import settings
from .spiders.proxy.kuaidaili_spider import fetch_proxy


class Helper(object):
    tz = pytz.timezone(settings.TIMEZONE)

    @classmethod
    def get_num_split_comma(cls, value):
        page = value.split(' ')
        return page[3].strip()

    @classmethod
    def get_star_split_str(cls, value):
        rate = value.split('out of 5 stars')   # 分割字符串
        return rate[0].strip()

    @classmethod
    def get_rate_split_str(cls, value):
        rate = value.split('customer ratings')  # 分割字符串
        return rate[0].strip()

    @classmethod
    def get_date_split_str(cls, value):
        return value.split('on')[1].strip()

    @classmethod
    def convert_date_str(cls, date_str):
        return datetime.datetime.strptime(date_str, '%B %d, %Y')

    @classmethod
    def delay_forty_days(cls):
        now = datetime.datetime.now()
        delay14 = now + datetime.timedelta(days=-40)  # 计算往前40天之后的时间
        return delay14

    @classmethod
    def get_rank_classify(cls, spider_str):
        result = re.match(r'#([0-9,]+)(?:.*)in (.*) \(.*[Ss]ee [Tt]op.*\)', spider_str)
        return result.groups()

    @classmethod
    def get_keyword_page_num(cls, rank):
        page_num = ceil(int(rank) / 16)
        return page_num

    @classmethod
    def get_keyword_page_range(cls, page_num):
        return range(page_num - 4 if page_num - 4 > 0 else 1, page_num + 4 if page_num + 4 <= 20 else 20)

    @classmethod
    def random_str(cls, randomlength):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(randomlength):
            str += chars[random.randint(0, length)]
        return str

    @classmethod
    def get_now_date(cls):
        now = datetime.datetime.now(cls.tz).strftime('%Y-%m-%d %H:%M:%S')
        return now

    @classmethod
    def is_set(cls, variable):
        try:
            type(eval(variable))
        except:
            return 0
        else:
            return 1

    @classmethod
    def filter_emoji(cls, desstr, restr=''):
        # 过滤表情
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub(restr, desstr)

    @classmethod
    def get_cookies(cls, cookie_file):
        # 从文件中获取保存的cookies
        with open(cookie_file, 'r', encoding='utf-8') as f:
            list_cookies = json.loads(f.read())  # 获取cookies

        cookies_str = "{'"
        for cookie in list_cookies:
            # 在保存成dict时，我们其实只要cookies中的name和value，而domain等其他都可以不要
            cookies_str = cookies_str + cookie['name'] + "=" + cookie['value'] + '; '
        cookies_str = cookies_str + "'}"

        return cookies_str

    @classmethod
    def redis(cls):
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
                        password=settings.REDIS_PASSWORD, decode_responses=True)

        return r

    # 从缓存取代理
    @classmethod
    def proxy_ready(cls, redis):
        proxy_list = redis.get(settings.PROXY_LIST)
        if proxy_list is None:
            proxy_list = fetch_proxy()  # 获取代理
            redis.setex(settings.PROXY_LIST, 600, ','.join(proxy_list))

            # 缓存代理不存在，则提示机器人
            redis.setex(settings.IS_ROBOT, 600, 1)
        else:
            proxy_list = proxy_list.split(',')

        while True:
            proxy = random.choice(proxy_list)
            key = proxy + settings.BOT_NAME
            if redis.exists(key):
                pass
            else:
               break

        # 控制一个IP在1S内只被使用一次
        redis.setex(key, 1, 5)
        return proxy

    #  更新缓存的代理
    @classmethod
    def update_proxy(cls, redis, expire_proxy):
        proxy_list = redis.get(settings.PROXY_LIST)
        proxy_list = proxy_list.split(',')
        for proxy in proxy_list:
            if proxy != expire_proxy:
                proxy_list.remove(proxy)

        redis.setex(settings.PROXY_LIST, 600, ','.join(proxy_list))

    #  更新缓存的代理
    @classmethod
    def get_cookie(cls, cookie_file):
        with open(cookie_file, 'r') as f:
            p = re.compile(r'<Cookie (.*?) for .*?>')
            cookies = re.findall(p, f.read())
            cookies = (cookie.split('=', 1) for cookie in cookies)
            cookies = dict(cookies)

        return cookies