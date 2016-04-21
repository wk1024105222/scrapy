# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from tencentjob.items import TencentjobItem
import sys

class TencentCrawlerSpider(CrawlSpider):
    '''
    递归 爬取 腾讯招聘  职位信息
    '''
    name = 'tencentjob_crawler'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?lid=&tid=&start=990#a']

    rules = [
        Rule(SgmlLinkExtractor(allow=r'/position.php\?lid=&tid=&start=\d{4}#a')),
        Rule(SgmlLinkExtractor(allow=r'/position_detail.php\?id=\d{1,5}&keywords=&tid=0&lid=0'),
                 callback='parse_item', follow=False),
    ]

    def parse_item(self, response):
        # print response.body
        item = TencentjobItem()
        detail = response.xpath('//table[@class="tablelist textl"][1]')
        if len(detail) == 1:
            try:
                item['url']=response.url
            except Exception as e:
                item['url']='error'
            try:
                item['name']=  detail.xpath('tr[1]/td/text()').extract()[0]
            except Exception as e:
                item['name']='error'
            try:
                item['addr']=detail.xpath('tr[2]/td[1]/text()').extract()[0]
            except Exception as e:
                item['addr']='error'
            try:
                item['type']=detail.xpath('tr[2]/td[2]/text()').extract()[0]
            except Exception as e:
                item['type']='error'
            try:
                item['num']=detail.xpath('tr[2]/td[3]/text()').extract()[0]
            except Exception as e:
                item['num']='error'
            try:
                str = ''
                for tmp in detail.xpath('tr[3]/td/ul/li'):
                    str=str+'\n'+tmp.xpath('text()').extract()[0]
                item['detail1']=str
            except Exception as e:
                item['detail1']='error'
            try:
                str = ''
                for tmp in detail.xpath('tr[4]/td/ul/li'):
                    str=str+'\n'+tmp.xpath('text()').extract()[0]
                item['detail2']=str
            except Exception as e:
                item['detail2']='error'
            # print response.url
            # print detail.xpath('tr[1]/td/text()').extract()[0]
            # print detail.xpath('tr[2]/td[1]/text()').extract()[0]
            # print detail.xpath('tr[2]/td[2]/text()').extract()[0]
            # print detail.xpath('tr[2]/td[3]/text()').extract()[0]
            # str = ''
            # for tmp in detail.xpath('tr[3]/td/ul/li'):
            #     str=str+'\n'+tmp.xpath('text()').extract()[0]
            # print str
            # str = ''
            # for tmp in detail.xpath('tr[4]/td/ul/li'):
            #     str=str+'\n'+tmp.xpath('text()').extract()[0]
            # print str
            return item
