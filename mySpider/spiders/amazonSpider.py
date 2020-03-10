# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..sql import TeacherSql
from mySpider.items import AmazonItem


class AmazonspiderSpider(CrawlSpider):
    name = 'amazonSpider'
    allowed_domains = ['amazon.cn']
    start_urls = ['https://www.amazon.cn']

    # rules = (
    #     Rule(LinkExtractor(allow=r'.*/dp/[0-9A-Z]{10}.*'), callback='parse_detail', follow=True),
    # )

    def parse(self, response):
        item = {}
        # 商品标题
        item['product_title'] = response.xpath('//span[@id="productTitle"]/text()').get().strip()
        # 标签
        item['product_tags'] = response.xpath('//div[@class="badge-wrapper "]/i/text()').get()
        # 价格
        item['product_price'] = response.xpath('//span[@id="priceblock_dealprice"]/text()').get().replace('￥', '')
        # 库存状态
        item['stock_status'] = response.xpath('//span[@id="ddmAvailabilityMessage"]/span/text()').get()
        # 销售配送
        item['sales'] = response.xpath('//div[@id="ddmMerchantMessage"]/text()').get()

        item['technical_details'] = response.xpath('div[@id="prodDetails"]/text()').get()

        item['create_time'] = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime(time.time()))

        TeacherSql.insert_amazon_product_item(item)
        yield item

    def parse_detail(self, response):
        item = {}
        # 商品标题
        item['product_title'] = response.xpath('//span[@id="productTitle"]/text()').get().strip()
        # 标签
        item['product_tags'] = response.xpath('//div[@class="badge-wrapper "]/i/text()').get()
        # 价格
        item['product_price'] = response.xpath('//span[@id="priceblock_dealprice"]/text()').get().replace('￥', '')
        # 库存状态
        item['stock_status'] = response.xpath('//span[@id="ddmAvailabilityMessage"]/span/text()').get()
        # 销售配送
        item['sales'] = response.xpath('//div[@id="ddmMerchantMessage"]/text()').get()

        item['technical_details'] = response.xpath('div[@id="prodDetails"]/text()').get()

        item['create_time'] = time.strftime('%Y-%m-%d %H:%I:%S', time.localtime(time.time()))
        TeacherSql.insert_amazon_product_item(item)
        yield item
        # return item
