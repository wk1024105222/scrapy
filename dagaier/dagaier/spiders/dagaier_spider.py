# -*- coding: utf-8 -*-
import logging

from scrapy import Spider, Request
import sys
from dagaier.items import DagaierItem

sys.stdout=open('output.txt','w') #将打印信息输出在相应的位置下

logging.basicConfig(level=logging.INFO,
                filemode='w',
                format='%(asctime)s %(thread)d [line:%(lineno)d] [%(threadName)s] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='dagaier_spider.log')
baseurl = 'http://dd.ghuws.men'
#baseurl = 'http://dc.itbb.men'
class DagaierCrawlerSpider(Spider):
    name = 'dagaier_spider'
    allowed_domains = [baseurl]
    # start_urls = ['https://gz.lianjia.com/ershoufang/pg1c219999216554095/','https://gz.lianjia.com/ershoufang/pg1c2111103316916/']
    #生成190页索引页的url
    start_urls = [baseurl+'/thread0806.php?fid=16&search=&page='+str(i)+'' for i in range(1,6,1)]

    def parse(self, response):
        '''
        c从每个索引页中获取帖子url
        :param response:
        :return:
        '''
        print response.url
        urls =  response.xpath('//h3/a/@href').extract()
        for url in urls:
            if url.startswith('htm_data') == True :
                print baseurl+'/'+url
                yield Request(baseurl+'/%s' % (url), callback=self.parse_item,dont_filter=True)

    def parse_item(self, response):
        item = DagaierItem()
        item['url']=response.url
        item['name'] =  response.xpath('//h4/text()').extract()[0]
        item['id'] = response.url.split('/')[-1]


        urls = response.xpath('//div[@class="tpc_content do_not_catch"]/input/@src').extract()
        if len(urls) == 0:
            urls = response.xpath('//p[@align="center"]/input/@src').extract()
        item['pictures'] = urls
        return item







