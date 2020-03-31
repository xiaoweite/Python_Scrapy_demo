# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mySpider.items import ZbpPostItem



class XiaoweiteSpider(CrawlSpider):
    name = 'xiaoweite'
    allowed_domains = ['blog.csdn.net']
    start_urls = ['https://blog.csdn.net/xiaoweite1',
                  'https://blog.csdn.net/xiaoweite1/article/list/2',
                  'https://blog.csdn.net/xiaoweite1/article/list/3',
                  'https://blog.csdn.net/xiaoweite1/article/list/4',
                  'https://blog.csdn.net/xiaoweite1/article/list/5',
                  'https://blog.csdn.net/xiaoweite1/article/list/6',
                  'https://blog.csdn.net/xiaoweite1/article/list/7'
                  ]

    rules = (
        Rule(LinkExtractor(allow=r'.+xiaoweite1\/article\/list\/\d+'),follow=True),
        Rule(LinkExtractor(allow=r'.+xiaoweite1\/article\/details\/\d+'), callback='parse_item', follow=False),
    )


    def parse_item(self, response):
        print('parse_item comming')

        # 分类ID
        log_CateID = 2
        # 作者ID
        log_AuthorID = 1
        # 标题
        log_Title = response.xpath("//h1[@class='title-article']/text()").get()
        # 摘要
        log_Intro = response.xpath("//h1[@class='title-article']/text()").get()
        # 内容
        log_Content = response.xpath("//div[@id='content_views']").get()
        # 发布时间
        log_PostTime = int(time.time())

        log_Meta = ''


        item = ZbpPostItem(
            log_CateID=log_CateID,
            log_AuthorID=log_AuthorID,
            log_Title=log_Title,
            log_Intro=log_Intro,
            log_Content=log_Content,
            log_PostTime=log_PostTime,
            log_Meta=log_Meta
        )

        yield item

