# -*- coding: utf-8 -*-

from scrapy import Spider, Request
import json
from lianjia.items import SellHouseItem

# xiaoquids = open('xiaoquid.csv').readlines()
xiaoquids = []
urls=[]
for id in xiaoquids:
    urls.append('https://gz.lianjia.com/ershoufang/pg1c%s/' % (id.strip()))

class ZolNoteBookCrawlerSpider(Spider):

    name = 'lianjiahouse_spider2'
    allowed_domains = ['gz.lianjia.com']
    # start_urls = ['https://gz.lianjia.com/ershoufang/pg1c219999216554095/','https://gz.lianjia.com/ershoufang/pg1c2111103316916/']
    start_urls = urls

    def parse(self, response):
        print response.url
        pagesinfo =  response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()

        if len(pagesinfo) > 0:
            pagenum = json.loads(pagesinfo[0])['totalPage']
            if pagenum > 1:
                index1 = response.url.find('pg')
                if index1 != -1:
                    index2 = response.url.find('c',index1+2)
                    if index2 != -1:
                        before = response.url[0:index1+2]
                        after = response.url[index2:]
                        for a in range(2,pagenum+1,1):
                            newurl = '%s%d%s' % (before,a,after)
                            yield Request(newurl, callback=self.parse)


        item = SellHouseItem()
        houses = response.xpath('//li[@class="clear"]/div[@class="info clear"]')

        for house in houses:
            try:
                item['url']=house.xpath('div[@class="title"]/a/@href').extract()[0]
                item['title']= house.xpath('div[@class="title"]/a/text()').extract()[0]

                address = (house.xpath('div[@class="address"]/div[@class="houseInfo"]/a/text()').extract()[0] +\
                          house.xpath('div[@class="address"]/div[@class="houseInfo"]/text()').extract()[0]).split('|')
                if len(address) >=1:
                    item['xiaoqu']=address[0]
                if len(address) >=2:
                    item['layout']=address[1]
                if len(address) >=3:
                    item['area']=address[2]
                if len(address) >=4:
                    item['direction']=address[3]
                if len(address) >=5:
                    item['style']=address[4]
                if len(address) >=6:
                    item['lift']= address[5]

                item['addr']=house.xpath('div[@class="flood"]/div[@class="positionInfo"]/a/text()').extract()[0]
                tmp = house.xpath('div[@class="flood"]/div[@class="positionInfo"]/text()').extract()[0]
                item['floor']= tmp[0:tmp.find(')')+1]
                item['year']=tmp[tmp.find(')')+1:-4]
                tmp = []
                tmp = house.xpath('div[@class="followInfo"]/text()').extract()[0].split('/')

                if len(tmp) >=1:
                    item['care']=tmp[0]
                if len(tmp) >=2:
                    item['visit']=tmp[1]
                if len(tmp) >=3:
                    item['publish']=tmp[2]
                item['price']=house.xpath('div[@class="priceInfo"]//div[@class="totalPrice"]/span/text()').extract()[0]
            except IndexError :
                print IndexError
            else:
                yield item

