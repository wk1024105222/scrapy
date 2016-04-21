# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from lianjia.items import HouseItem
import sys

sys.stdout=open('output.txt','w') #将打印信息输出在相应的位置下

class LianjiaHouseCrawlerSpider(CrawlSpider):
    '''
    递归 爬取 广州  链家 二手房信息 以文本形式保存到本地
    start_urls 写的简单 导致爬虫访问量上升
    rules 越精确 爬虫访问量越少
     '''
    name = 'lianjiahouse_crawler'
    allowed_domains = ['gz.lianjia.com']
    start_urls = [ 'http://gz.lianjia.com/ershoufang/pg'+str(i) for i in range(1,101,1)]+\
                 [ 'http://gz.lianjia.com/ershoufang/p'+str(i) for i in range(1,9,1)]+\
                 [ 'http://gz.lianjia.com/ershoufang/a'+str(i) for i in range(1,8,1)]+\
                 [ 'http://gz.lianjia.com/ershoufang/l'+str(i) for i in range(1,7,1)]+\
                 [ 'http://gz.lianjia.com/ershoufang/lc'+str(i) for i in range(1,4,1)]+\
                 [ 'http://gz.lianjia.com/ershoufang/f'+str(i) for i in range(1,6,1)]+\
                 [ 'http://gz.lianjia.com/ershoufang/y'+str(i) for i in range(1,5,1)]+\
                 ['http://gz.lianjia.com/ditiefang/li1104606'+str(i) for i in range(79,89,1)]+\
                 [ 'http://gz.lianjia.com/ditiefang/mt'+str(i) for i in range(1,4,1)]
    rules = [
        Rule(SgmlLinkExtractor(allow=r'/ershoufang/[a-z]{,30}/?$')),
        Rule(SgmlLinkExtractor(allow=r'/xiaoqu/[0-9]{,15}/esf/?$')),
        # Rule(SgmlLinkExtractor(allow=r'/ershoufang/pg\d')),
        Rule(SgmlLinkExtractor(allow=r'/ershoufang/GZ\d{,10}\.html$'),
                 callback='parse_item', follow=True),
    ]

    def parse_item(self, response):
        # print response.body
        item = HouseItem()
        try:
            item['url'] = response.url
        except Exception as e:
            item['url']='error'
        try:
            item['title'] = response.xpath('//h1[@class="main"]/text()').extract()[0]
        except Exception as e:
            item['title']='error'
        try:
            item['xiaoqu'] = response.xpath('//div[@class="communityName"]/a[@class="info"]/text()').extract()[0]
        except Exception as e:
            item['xiaoqu']='error'
        try:
            item['layout'] = response.xpath('//div[@class="room"]/div[@class="mainInfo"]/text()').extract()[0]
        except Exception as e:
            item['layout']='error'
        try:
            item['area'] = response.xpath('//div[@class="area"]/div[@class="mainInfo"]/text()').extract()[0]
        except Exception as e:
            item['area']='error'
        try:
            item['direction'] = response.xpath('//div[@class="type"]/div[@class="mainInfo"]/text()').extract()[0]
        except Exception as e:
            item['direction']='error'
        try:
            item['addr'] = response.xpath('//div[@class="areaName"]/span[@class="info"]/a[1]/text()').extract()[0]\
                           +response.xpath('//div[@class="areaName"]/span[@class="info"]/a[1]/text()').extract()[0]
        except Exception as e:
            item['addr']='error'
        try:
            item['floor'] = response.xpath('//div[@class="room"]/div[@class="subInfo"]/text()').extract()[0]
        except Exception as e:
            item['floor']='error'
        try:
            item['year'] = response.xpath('//div[@class="area"]/div[@class="subInfo"]/text()').extract()[0]
        except Exception as e:
            item['year']='error'
        try:
            item['price'] = response.xpath('//span[@class="total"]/text()').extract()[0]
        except Exception as e:
            item['price']='error'
        try:
            item['visit'] = response.xpath('//div[@class="panel"]/div[@class="totalCount"]/span/text()').extract()[0]
        except Exception as e:
            item['visit']='error'
        try:
            item['style'] = response.xpath('//div[@class="type"]/div[@class="subInfo"]/text()').extract()[0]
        except Exception as e:
            item['style']='error'


        return item
