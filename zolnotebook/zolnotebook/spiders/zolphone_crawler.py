# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zolnotebook.items import ZolnotebookItem

class ZolphoneCrawlerSpider(CrawlSpider):
    """
    从中关村在线下载手机数据
    本程序 用CrawlSpider 下载id
    后续编写新的爬虫 根据id 生成url 获取配置信息
    """
    name = 'zolphone_crawler'
    allowed_domains = ['detail.zol.com.cn']
    start_urls = [ 'http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html']

    rules = [Rule(LinkExtractor(allow=r'/cell_phone_index/subcate57[a-z0-9_]*?\.html'),callback='parse_item', follow=True), ]

    def parse_item(self, response):
        # print '============================================================================================'
        # print response.body
        ids =  response.xpath('//li[@data-follow-id]/@data-follow-id').extract()
        prices = response.xpath('//b[@class="price-type"]/text()').extract()
        length = len(ids)

        item = ZolnotebookItem()
        map = {}
        map['ids']=[]
        map['price']=[]
        map['url'] = response.url
        if len(prices) == length:
            for index in range(0, length, 1):
                map['ids'].append(ids[index][1:])
                map['price'].append(prices[index])
        else:
            for index in range(0, length, 1):
                map['id'].append(ids[index][1:])
            print response.url,'价格数量与ID数量不一致'
        item['param']=map


        return item