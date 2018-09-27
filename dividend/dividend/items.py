# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class DividendItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 公告日期
    # 分红年度
    # 送股
    # 转增
    # 派息
    # 股权登记日
    # 除权除息日
    # 红股上市日
    code  = Field()
    date1 = Field()
    year = Field()
    stockDividend =Field()
    transfeShares=Field()
    dividendPayout=Field()
    date2 = Field()
    date3 = Field()
    date4 = Field()


    pass
