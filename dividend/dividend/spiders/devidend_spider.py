# -*- coding: utf-8 -*-
import logging

from scrapy import Spider, Request
import sys
from dividend.items import DividendItem
from picture.dbpool import pool

# sys.stdout=open('output.txt','w') #将打印信息输出在相应的位置下
logging.basicConfig(level=logging.INFO,
                filemode='w',
                format='%(asctime)s %(thread)d [line:%(lineno)d] [%(threadName)s] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='devidend_spider.log')

# 缓存所有已下载的页面数据
con = pool.connection()
cursor = con.cursor()
cursor.execute("select code from STOCKINFO")
allcodes = []
for url in cursor.fetchall():
    allcodes.append(url[0])
con.close()

class PictureCrawlerSpider(Spider):
    name = 'devidend_spider'
    allowed_domains = ['http://quotes.money.163.com/f10']
    #生成索引页的url
    start_urls = ['http://quotes.money.163.com/f10/fhpg_'+code+'.html' for code in allcodes]

    def parse(self, response):
        result = []
        items = response.xpath('//table[@class="table_bg001 border_box limit_sale"]')[0].xpath('tr')
        code = response.xpath('//h1[@class="name"]/span/a/text()').extract()[0]
        for tmp in items :
            texts = tmp.xpath('td/text()').extract()
            item = DividendItem()
            item['code'] = code
            item['date1'] = texts[0]
            item['year'] = texts[1]
            item['stockDividend'] = texts[2]
            item['transfeShares'] = texts[3]
            item['dividendPayout'] = texts[4]
            item['date2'] = texts[5]
            item['date3'] = texts[6]
            item['date4'] = texts[7]
            result.append(item)
        return result







