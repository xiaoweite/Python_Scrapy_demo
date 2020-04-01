# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

class MyspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    cookies = {
        'uuid_tt_dd': '10_19030931310-1582300934803-370416',
        'dc_session_id': '10_1582300934803.989237',
        'UN': 'xiaoweite1',
        'Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac': '6525*1*10_19030931310-1582300934803-370416!5744*1*xiaoweite1',
        'UM_distinctid': '170772dcba444-08fed927ee8fd3-6313f69-1fa400-170772dcba5337',
        'c_ref': 'https%3A//lansonli.blog.csdn.net/',
        'dc_sid': '11e6bff210da119d7b46a3b62f8b521b',
        'Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac': 1584458680,
        'announcement': '%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fblog.csdn.net%252Fblogdevteam%252Farticle%252Fdetails%252F105203745%2522%252C%2522announcementCount%2522%253A1%252C%2522announcementExpire%2522%253A156984342%257D',
        'c-login-auto': 1,
        'firstDie': 1,
        'c-toolbar-writeguide': 1,
        'SESSION': '49cff2fc-2fac-4147-a437-acf00bb58b6c',
        'dc_tos': 'q82gqq',
        'Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac': 1585672515,
        'UserName': 'xiaoweite1',
        'UserInfo': '8c2bf37da1e440f28d8b22d913ea8b10',
        'UserToken': '8c2bf37da1e440f28d8b22d913ea8b10',
        'UserNick': 'Lansonli',
        'AU': '00A',
        'BT': 1585672575167,
        'p_uid': 'U100000'
    }

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s



    def process_request(self, request, spider):

        request.cookies = self.cookies
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        #return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



