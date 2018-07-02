# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from picture.items import PictureItem

class PictureSpider(CrawlSpider):
    name = 'picture_crawler'
    allowed_domains = ['cl.giit.us']
    start_urls = ['http://dc.ddder.us/thread0806.php?fid=16&search=&page='+str(i)+'' for i in range(1,10,1)]

    rules = (
        Rule(LinkExtractor(allow=r'htm_data/\d{2}/\d{4}/\d{7}\.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = PictureItem()
        item['url']=response.url
        item['name'] =  response.xpath('//h4/text()').extract()[0]
        urls = response.xpath('//p[@align="center"]/input/@src').extract()
        if len(urls) == 0:
            # print response.url,'     len(urls) == 0'
            return
        else:
            item['pictures'] = urls
        # print response.url
        return item
