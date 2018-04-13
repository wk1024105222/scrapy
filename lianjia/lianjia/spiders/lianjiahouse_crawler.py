# -*- coding: utf-8 -*-
import logging
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from lianjia.items import HouseItem
import sys

logging.basicConfig(level=logging.INFO,
                filemode='w',
                format='%(asctime)s %(thread)d [line:%(lineno)d] [%(threadName)s] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='lianjiahouse_crawler.log')

# sys.stdout=open('output.txt','w') #将打印信息输出在相应的位置下
#    V2.0 遍历组合多种查询条件  生成url填充start_urls
quyu=['tianhe','yuexiu','liwan','haizhu','fanyu','baiyun','huangpugz','conghua','zengcheng','huadou','luogang','nansha','qita']
jiage=['p'+str(i) for i in range(1,9,1)]
mianji=['a'+str(i) for i in range(1,8,1)]
# fangxing=['l'+str(i) for i in range(1,7,1)]
ditie=['li1104606'+str(i) for i in range(79,89,1)]
url1=[]
for a in quyu:
    for b in jiage:
        for c in mianji:
            url1.append('http://gz.lianjia.com/ershoufang/%s/%s%s/' % (a,b,c))
            # print 'http://gz.lianjia.com/ershoufang/%s/%s%s/' % (a,b,c)
for e in ditie:
    for f in jiage:
        url1.append('http://gz.lianjia.com/ditiefang/%s/%s/' % (e,f))
        # print 'http://gz.lianjia.com/ditiefang/%s/%s/' % (e,f)


class LianjiaHouseCrawlerSpider(CrawlSpider):
    '''
    递归 爬取 广州  链家 二手房信息 以文本形式保存到本地
    start_urls 写的简单 导致爬虫访问量上升
    rules 越精确 爬虫访问量越少
     '''
    name = 'lianjiahouse_crawler'
    allowed_domains = ['gz.lianjia.com']
    #    V1.0
    # start_urls = [ 'http://gz.lianjia.com/ershoufang/pg'+str(i) for i in range(1,101,1)]+\
    #              [ 'http://gz.lianjia.com/ershoufang/p'+str(i) for i in range(1,9,1)]+\
    #              [ 'http://gz.lianjia.com/ershoufang/a'+str(i) for i in range(1,8,1)]+\
    #              [ 'http://gz.lianjia.com/ershoufang/l'+str(i) for i in range(1,7,1)]+\
    #              [ 'http://gz.lianjia.com/ershoufang/lc'+str(i) for i in range(1,4,1)]+\
    #              [ 'http://gz.lianjia.com/ershoufang/f'+str(i) for i in range(1,6,1)]+\
    #              [ 'http://gz.lianjia.com/ershoufang/y'+str(i) for i in range(1,5,1)]+\
    #              ['http://gz.lianjia.com/ditiefang/li1104606'+str(i) for i in range(79,89,1)]+\
    #              [ 'http://gz.lianjia.com/ditiefang/mt'+str(i) for i in range(1,4,1)]
    #    V2.0
    start_urls = url1
    #    V3.0
    # start_urls=['http://gz.lianjia.com/ershoufang']
    rules = [
        #    V1.0、V2.0
        Rule(LinkExtractor(allow=r'/ershoufang/[a-z]{,30}/?$')),
         Rule(LinkExtractor(allow=r'/ershoufang/[0-9]{,20}/?$')),
        Rule(LinkExtractor(allow=r'/xiaoqu/[0-9]{,15}/esf/?$')),

        Rule(LinkExtractor(allow=r'/ershoufang/[GZ0-9]{2}\d{,10}\.html$'),
                 callback='parse_item', follow=True),
        #    V3.0
        # Rule(LinkExtractor(allow=r'/ershoufang/\w*?')),

    ]

    def parse_item(self, response):
        print response.url
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
            item['xiaoqu'] = response.xpath('//div[@class="communityName"]/a[@class="info "]/text()').extract()[0]
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
                           +response.xpath('//div[@class="areaName"]/span[@class="info"]/a[2]/text()').extract()[0]
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
