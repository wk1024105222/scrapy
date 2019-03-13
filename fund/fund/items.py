# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class FundBaseInfoItem(Item):
    url = Field()
    code = Field()
    type = Field()
    fullName = Field()
    name = Field()
    type = Field()
    issueDate = Field()
    listDate = Field()
    company = Field()
    manager = Field()
    bank = Field()
    bonus = Field()
    manageRate = Field()
    trusteeshipRate = Field()

class FundAssetAllocationItem(Item):
    url = Field()
    code = Field()
    type = Field()
    date = Field()
    stockPer = Field()
    bondPer = Field()
    cashPer = Field()
    netAssets = Field()

class FundAssetsScaleItem(Item):
    url = Field()
    code = Field()
    type = Field()
    date = Field()
    applyNum = Field()
    redeemNum = Field()
    totalNum = Field()
    balance = Field()
    changeRate = Field()


