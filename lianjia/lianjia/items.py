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
    # 塔楼
    houseType=Field()

    # 平米价格
    unitPrice= Field()
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

class SchoolItem(Item):
    id = Field()
    type = Field()
    # 链接
    url=Field()
    name = Field()  # 名称
    alias = Field()  # 别名
    primaryMiddle = Field()  # 小学中学
    rank = Field()  # 等级省级=Field() #市级。。
    statePrivare = Field()  # 公立私立
    addr = Field()  # 地址
    featureTag = Field()  # 特色
    tel = Field()  # 电话
    toSchool = Field()  # 对口学校


class RecruitStudentsItem(Item):
    id = Field()
    url = Field()
    type = Field()
    introduce = Field()  # 学校介绍
    scope = Field()  # 招生范围
    brochure = Field()  # 招生简章
    require = Field()  # 入学条件
    feature = Field()  # 学校特色描述



