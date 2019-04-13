# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SellHouseItem(Item):
    type = Field()
    url=Field()
    # 房屋标题
    title=Field()
    # 房屋code
    id = Field()
    # 小区名称
    xiaoqu=Field()
    # 小区id
    xiaoquID = Field()
    # 格局
    layout=Field()
    # 面积
    area=Field()
    # 朝向
    direction=Field()
    # 地址
    addr=Field()
    # 楼层
    floor=Field()
    # 建楼时间
    year=Field()
    # 价格
    price=Field()
    # 带看数量
    visit=Field()
    # 装修类型
    style=Field()
    # 电梯
    lift=Field()
    # 关注数量
    care=Field()
    publish = Field()

class DealHouseItem(Item):
    type = Field()
    url=Field()
    # 房屋code
    id = Field()
    # 小区id
    xiaoquID = Field()
    # 挂牌价格
    listPrice = Field()
    # 成交价格
    dealPrice = Field()
    # 成交周期
    dealDays = Field()
    # 成交时间
    dealDate = Field()
    # 每平米价格
    averagePrice= Field()

class XiaoquItem(Item):
    type = Field()
    # 链接
    url=Field()
    # 小区名称
    name=Field()
    # 小区均价
    price=Field()
    # 小区ID
    id = Field()
    # 在售数量
    sellCount = Field()
    # 出租数量
    rentCount = Field()
    # 90天成交数量
    dealCount90d = Field()
    # 建筑时间
    buidYear = Field()


