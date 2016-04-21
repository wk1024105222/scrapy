# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TencentjobItem(Item):
    url=Field()
    name = Field()
    type = Field()
    num=Field()
    addr=Field()

    detail1=Field()
    detail2=Field()



