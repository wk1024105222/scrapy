# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class HouseItem(Item):
    url=Field()
    title=Field()

    xiaoqu=Field()
    layout=Field()
    area=Field()
    direction=Field()

    addr=Field()
    floor=Field()
    year=Field()

    price=Field()

    visit=Field()

    style=Field()


