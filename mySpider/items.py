# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ItcastItem(scrapy.Item):
    # 姓名
    name = scrapy.Field()
    # 职称
    title = scrapy.Field()
    # 个人简介
    info = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()

class AmazonItem(scrapy.Item):
    # 商品标题
    product_title = scrapy.Field()
    # 标签
    product_tags = scrapy.Field()
    # 价格
    product_price = scrapy.Field()
    # 库存状态
    stock_status = scrapy.Field()
    # 销售配送
    sales = scrapy.Field()

    technical_details = scrapy.Field()

