# -*- coding: utf-8 -*-
import logging

from scrapy import Spider, Request
import sys
from fund.dbpool import pool
from fund.items import FundBaseInfoItem

sys.stdout=open('output.txt','w') #将打印信息输出在相应的位置下

logging.basicConfig(level=logging.INFO,
                filemode='w',
                format='%(asctime)s %(thread)d [line:%(lineno)d] [%(threadName)s] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='fund_spider.log')

# 获取未下载的页面
con = pool.connection()
cursor = con.cursor()
cursor.execute("select url from fund_dataurl where type='jbgk' and flag='0'")
urls = []
for url in cursor.fetchall():
    urls.append(url[0])
con.close()

baseurl = 'http://fundf10.eastmoney.com'

class FundCrawlerSpider(Spider):
    name = 'fund_spider'
    allowed_domains = [baseurl]
    start_urls = urls

    def parse(self, response):
        url = response.url
        item = None
        if url.find('jbgk') >= 0:
            try:
                item = FundBaseInfoItem()
                tr0 = response.xpath('//*[@class="info w790"]/tr[1]')
                tr1 = response.xpath('//*[@class="info w790"]/tr[2]')
                tr2 = response.xpath('//*[@class="info w790"]/tr[3]')
                tr4 = response.xpath('//*[@class="info w790"]/tr[5]')
                tr5 = response.xpath('//*[@class="info w790"]/tr[6]')
                tr6 = response.xpath('//*[@class="info w790"]/tr[7]')
                item['url'] = response.url
                item['code'] = url[-11:-5]
                item['fullName'] = tr0.xpath('td[1]/text()').extract()[0]
                item['name'] = tr0.xpath('td[2]/text()').extract()[0]
                item['type'] = tr1.xpath('td[2]/text()').extract()[0]
                item['issueDate'] = tr2.xpath('td[1]/text()').extract()[0]
                item['listDate'] = tr2.xpath('td[2]/text()').extract()[0]
                item['manageRate'] = tr6.xpath('td[1]/text()').extract()[0]
                item['trusteeshipRate'] = tr6.xpath('td[2]/text()').extract()[0]

                item['company'] = tr4.xpath('td[1]/a/text()').extract()[0]
                item['manager'] = tr5.xpath('td[1]/a/text()').extract()[0]
                item['bank'] = tr4.xpath('td[2]/a/text()').extract()[0]
                item['bonus'] = tr5.xpath('td[2]/a/text()').extract()[0]

                yield item
            except Exception as e:
                print '解析异常'+response.url

    def parse_item(self, response):
        url = response.url
        item = None
        if url.find('jbgk')>=0:
            item = FundBaseInfoItem()
            tr0 = response.xpath('//*[@class="info w790"]/tr[1]')
            tr1 = response.xpath('//*[@class="info w790"]/tr[2]')
            tr2 = response.xpath('//*[@class="info w790"]/tr[3]')
            tr4 = response.xpath('//*[@class="info w790"]/tr[5]')
            tr5 = response.xpath('//*[@class="info w790"]/tr[6]')
            tr6 = response.xpath('//*[@class="info w790"]/tr[7]')
            item['url'] = response.url
            item['code'] = url[-11:-5]
            item['fullName'] = tr0.xpath('td[1]/text()').extract()[0]
            item['name'] = tr0.xpath('td[2]/text()').extract()[0]
            item['type'] = tr1.xpath('td[2]/text()').extract()[0]
            item['issueDate'] = tr2.xpath('td[1]/text()').extract()[0]
            item['listDate'] = tr2.xpath('td[2]/text()').extract()[0]
            item['manageRate'] = tr6.xpath('td[1]/text()').extract()[0]
            item['trusteeshipRate'] = tr6.xpath('td[2]/text()').extract()[0]

            item['company'] = tr4.xpath('td[1]/a/text()').extract()[0]
            item['manager'] = tr5.xpath('td[1]/a/text()').extract()[0]
            item['bank'] = tr4.xpath('td[2]/a/text()').extract()[0]
            item['bonus'] = tr5.xpath('td[2]/a/text()').extract()[0]
        return item







