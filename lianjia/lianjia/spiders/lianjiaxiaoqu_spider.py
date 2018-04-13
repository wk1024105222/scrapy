# -*- coding: utf-8 -*-
import logging

from scrapy import Spider
from lianjia.items import HouseItem, XiaoquItem

logging.basicConfig(level=logging.INFO,
                filemode='w',
                format='%(asctime)s %(thread)d [line:%(lineno)d] [%(threadName)s] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='lianjiaxiaoqu_spider.log')

quyu=['tianhe','yuexiu','liwan','haizhu','fanyu','baiyun','huangpugz','conghua','zengcheng','huadou','nansha']
pagesize=[38,45,31,40,39,32,11,3,10,19,5]

urls=[]
for num in range(0,11,1):
    for b in range(1,pagesize[num]+1,1):
        urls.append('https://gz.lianjia.com/xiaoqu/%s/pg%s/' % (quyu[num],b))


class StackCrawlerSpider(Spider):
    '''
    非递归 爬取链家 小区信息
    后续可根据小区信息 直接爬取在售房源、已售房源、在租房源
    start_urls 指定100页的url 最多爬取3000条的数据
    通过分析直接生成 小区列表页面url

    小区页面https://gz.lianjia.com/xiaoqu/2110343238336894/
    在售页面https://gz.lianjia.com/ershoufang/c2110343238336894/
    已售页面https://gz.lianjia.com/chengjiao/c2110343238336894/
    租房页面https://gz.lianjia.com/zufang/c2110343238336894/
    '''
    name = 'lianjiaxiaoqu_spider'
    allowed_domains = ['gz.lianjia.com']
    start_urls = urls

    def parse(self, response):
        xiaoqus = response.xpath('//li[@class="clear xiaoquListItem"]')
        items = []
        count=0
        for xiaoqu in xiaoqus:
            item = XiaoquItem()

            try:
                item['url'] = xiaoqu.xpath('a[@class="img"]/@href').extract()[0]
            except Exception as e:
                item['url']='error'
            try:
                item['name'] = xiaoqu.xpath('div[@class="info"]/div[@class="title"]/a/text()').extract()[0]
            except Exception as e:
                item['name']='error'
            try:
                item['price'] =  xiaoqu.xpath('div[@class="xiaoquListItemRight"]/div[@class="xiaoquListItemPrice"]'
                                              '/div[@class="totalPrice"]/span/text()').extract()[0]
            except Exception as e:
                item['price']='error'
            items.append(item)

        return items




