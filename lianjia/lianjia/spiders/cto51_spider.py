# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.utils.project import get_project_settings

from scrapy import conf


from scrapy import Spider
from lianjia.items import HouseItem
import sys

sys.stdout=open('output.txt','w') #将打印信息输出在相应的位置下


class StackCrawlerSpider(Spider):
    name = '51ctoScrapy'
    allowed_domains = ['www.tuicool.com']
    start_urls = [ 'http://www.tuicool.com/topics/11020113?st=0&lang=1&pn=' +str(i) for i in range(0,8,1)]

    # allowed_domains = ['baidu.com']
    # start_urls = [
    #     'http://www.baidu.com'
    # ]

    # rules = [
    #     Rule(SgmlLinkExtractor(allow=(r'/ershoufang/pg\d{1,3}/')), follow=False, callback='parse_item')
    # ]
    count=0
    def parse(self, response):
        print response.url
        print response.body
        print '#'*100
        # titles = response.xpath('//div[@class="article_title abs-title"]/a/text()')
        # items = []
        # count=0
        # for title in titles:
        #
        #     print title.extract()[0]
        # return items




