# -*- coding: utf-8 -*-

from scrapy import Spider
from lianjia.items import SellHouseItem
import sys

# sys.stdout=open('output.txt','w') #将打印信息输出在相应的位置下

class StackCrawlerSpider(Spider):
    '''
    非递归 爬取链家 广州 二手房信息
    start_urls 指定100页的url 最多爬取3000条的数据
    '''
    name = 'lianjiahouse_spider'
    allowed_domains = ['gz.lianjia.com']#http://gz.lianjia.com/ershoufang/pg1
    start_urls = [ 'http://gz.lianjia.com/ershoufang/pg'+str(i) for i in range(1,101,1)]

    def parse(self, response):
        houses = response.xpath('//div[@class="info-panel"]')
        items = []
        count=0
        for house in houses:
            item = SellHouseItem()
            try:
                item['url'] = house.xpath('h2/a/@href').extract()[0]
            except Exception as e:
                item['url']='error'
            try:
                item['title'] = house.xpath('h2/a/text()').extract()[0]
            except Exception as e:
                item['title']='error'
            try:
                item['xiaoqu'] = house.xpath('div[1]/div[1]/a/span/text()').extract()[0]
            except Exception as e:
                item['xiaoqu']='error'
            try:
                item['layout'] = house.xpath('div[1]/div[1]/span[1]/span/text()').extract()[0]
            except Exception as e:
                item['layout']='error'
            try:
                item['area'] = house.xpath('div[1]/div[1]/span[2]/text()').extract()[0]
            except Exception as e:
                item['area']='error'
            try:
                item['direction'] = house.xpath('div[1]/div[1]/span[3]/text()').extract()[0]
            except Exception as e:
                item['direction']='error'
            try:
                item['addr'] = house.xpath('div[1]/div[2]/div[1]/a/text()').extract()[0]
            except Exception as e:
                item['addr']='error'
            try:
                item['floor'] = house.xpath('div[1]/div[2]/div[1]/text()[1]').extract()[0]
            except Exception as e:
                item['floor']='error'
            try:
                item['year'] = house.xpath('div[1]/div[2]/div[1]/text()[2]').extract()[0]
            except Exception as e:
                item['year']='error'
            try:
                item['price'] = house.xpath('div[2]/div[1]/span/text()').extract()[0]+house.xpath('div[2]/div[1]/text()').extract()[0]
            except Exception as e:
                item['price']='error'
            try:
                item['visit'] = house.xpath('div[3]/div/div[1]/span/text()').extract()[0]
            except Exception as e:
                item['visit']='error'
            items.append(item)
            count+=1
        print response.url,':',str(count)
        return items




