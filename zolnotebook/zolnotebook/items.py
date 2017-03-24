# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class ZolnotebookItem(scrapy.Item):
    # 页面html
    # html=Field()
    # 参数列表 map
    param=Field()

    # url = Field()
    #
    # name = Field()
