# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BookItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id=Field()
    # $x('//span[@class="bookmetaTitle"]/a/text()')
    name = Field()
    author = Field()
    pubdate = Field()
    press = Field()


class LibraryItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    indexno  = Field()
    libname = Field()
    libarea = Field()
    bookcount  = Field()