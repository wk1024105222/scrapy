# -*- coding: utf-8 -*-
import logging

from scrapy import Spider, Request
import sys
from dagaier.items import DagaierItem
from dagaier.dbpool import pool

sys.stdout=open('output.txt','w') #将打印信息输出在相应的位置下

logging.basicConfig(level=logging.INFO,
                filemode='w',
                format='%(asctime)s %(thread)d [line:%(lineno)d] [%(threadName)s] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='dagaier_spider.log')

# 缓存所有已下载的页面数据
con = pool.connection()
cursor = con.cursor()
cursor.execute("select pageid from dagaierpage")
allpageid = []
for url in cursor.fetchall():
    allpageid.append(url[0])
con.close()

baseurl = 'http://cl.cbcb.us'

class DagaierCrawlerSpider(Spider):
    name = 'dagaier_spider'
    allowed_domains = [baseurl]
    # start_urls = ['https://gz.lianjia.com/ershoufang/pg1c219999216554095/','https://gz.lianjia.com/ershoufang/pg1c2111103316916/']
    #生成190页索引页的url
    start_urls = [baseurl+'/thread0806.php?fid=16&search=&page='+str(i)+'' for i in range(1,101,1)]

    def parse(self, response):
        '''
        从每个索引页中获取帖子url
        :param response:
        :return:
        '''
        # print response.url
        urls =  response.xpath('//h3/a/@href').extract()
        for url in urls:
            if url.startswith('htm_data') == True :
                # 判断数据库是否已存在 只yield 数据库没有的
                pageid = url.split('/')[-1]
                if pageid not in allpageid:
                    print url.split('/')[-1]
                    yield Request(baseurl+'/%s' % (url), callback=self.parse_item,dont_filter=True)

    def parse_item(self, response):
        item = DagaierItem()
        item['url']=response.url
        item['name'] =  response.xpath('//h4/text()').extract()[0]
        item['id'] = response.url.split('/')[-1]

        # html数据落地
        name = item['id']+'.txt'
        file = open(name, 'w')
        file.write(response.body)
        file.close()

        urls = response.xpath('//div[@class="tpc_content do_not_catch"]/input/@src').extract()
        if len(urls) == 0:
            urls = response.xpath('//p[@align="center"]/input/@src').extract()
            # 新的格式
            if len(urls) == 0:
                urls = response.xpath("//input[@type='image']/@data-src").extract()
        item['pictures'] = urls
        return item







