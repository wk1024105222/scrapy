# -*- coding: utf-8 -*-
import json
import logging

from scrapy import Spider, Request
from lianjia.items import SellHouseItem, XiaoquItem, DealHouseItem

logger = logging.getLogger('lianjiaxiaoqu_spider3Logger')

quyu=['tianhe','yuexiu','liwan','haizhu','fanyu','baiyun','huangpugz','conghua','zengcheng','huadou','nansha']
# 逐个查看每个区小区数量  每页30个  计算页数
xiaoquNum = [1232,1356,936,1196,1082,1017,347,286,477,671,174]

urls=[]
for num in range(0,11,1):
    pagesize = xiaoquNum[num]/30+1
    for b in range(1,pagesize+1,1):
        urls.append('https://gz.lianjia.com/xiaoqu/%s/pg%s/' % (quyu[num],b))
# urls.append('https://gz.lianjia.com/xiaoqu/tianhe/pg1/')

class lianjiahouse_spider3(Spider):
    '''
    1、根据行政区名以及手工查看的每个区小区数 生成广州所有小区List页面的url
    2、获取每个小区的ID 并生成在售房源页面以及历史成交房源页面 的url
    3、爬取在售房源信息以及历史成交信息
    '''
    name = 'lianjiahouse_spider3'
    allowed_domains = ['gz.lianjia.com']
    start_urls = urls

    def parse(self, response):
        # 获取当前页面小区信息
        xiaoqus = response.xpath('//li[@class="clear xiaoquListItem"]')
        for xiaoqu in xiaoqus:
            item = XiaoquItem()
            item['type'] = 'XiaoquItem'
            try:
                item['url'] = xiaoqu.xpath('a[@class="img"]/@href').extract()[0]
            except Exception as e:
                item['url']='error'
            try:
                item['id'] = xiaoqu.xpath('@data-id').extract()[0]
            except Exception as e:
                item['id']='error'
            try:
                item['name'] = xiaoqu.xpath('div[@class="info"]/div[@class="title"]/a/text()').extract()[0]
            except Exception as e:
                item['name']='error'
            try:
                item['price'] =  xiaoqu.xpath('div[@class="xiaoquListItemRight"]/div[@class="xiaoquListItemPrice"]/div[@class="totalPrice"]/span/text()').extract()[0]
            except Exception as e:
                item['price']='error'
            try:
                item['sellCount'] =  xiaoqu.xpath('div[@class="xiaoquListItemRight"]/div[@class="xiaoquListItemSellCount"]/a/span/text()').extract()[0]
            except Exception as e:
                item['sellCount']='error'
            try:
                item['rentCount'] =  xiaoqu.xpath('div[@class="info"]/div[@class="houseInfo"]/a[2]/text()').extract()[0]
            except Exception as e:
                item['rentCount']='error'
            try:
                item['dealCount90d'] =  xiaoqu.xpath('div[@class="info"]/div[@class="houseInfo"]/a[1]/text()').extract()[0]
            except Exception as e:
                item['dealCount90d']='error'
            try:
                item['buidYear'] =  xiaoqu.xpath('div[@class="info"]/div[@class="positionInfo"]/text()[4]').extract()[0]
            except Exception as e:
                item['buidYear']='error'

            yield item
            # 爬取小区在售房源第一页
            if item['sellCount']!='0':
                yield Request('https://gz.lianjia.com/ershoufang/pg1c%s/' % (item['id']), callback=self.parse_sellHouseItemFromListPage, dont_filter=True)
            # 爬取小区成交记录第一页
            yield Request('https://gz.lianjia.com/chengjiao/pg1c%s/' % (item['id']), callback=self.parse_dealHouseItemFromListPage,dont_filter=True)
        # yield Request('https://gz.lianjia.com/ershoufang/c2110343238599609/', callback=self.parse_sellHouseItemFromListPage,
        #               dont_filter=True)

    def parse_sellHouseItemFromListPage(self, response):
        url = response.url;
        # 定位 共找到 291 套广州二手房 确认数量 如果小区 成交数量为0 则跳过 如果数量超过10000 则跳过
        try:
            sellNum = int(response.xpath('//h2[@class="total fl"]/span/text()').extract()[0])
            if sellNum >10000:
                logger.info('%s this page is guangzhou total sell page' % (url))
                return
            elif sellNum >30:
                index1 = url.find('pg')
                index2 = url.find('c', index1 + 2)
                before = url[0:index1 + 2]
                after = url[index2:]
                for a in range(2, sellNum/30 + 2, 1):
                    newurl = '%s%d%s' % (before, a, after)
                    yield Request(newurl, callback=self.parse_sellHouseItemFromListPage)
                    # print newurl
            elif sellNum == 0:
                logger.info('%s this xiaoqu 0 house on sell' % (url))
                return
        except Exception as e:
            logger.error('%s get dealNum error' % (url))
            return

        tmp1 = url.split('/')[-2]
        xiaoquID = tmp1[tmp1.find('c'):]
        # 开始解析在售房源信息
        item = SellHouseItem()
        houses = response.xpath('//li[@class="clear LOGVIEWDATA LOGCLICKDATA"]/div[@class="info clear"]')

        for house in houses:
            item['type'] = 'SellHouseItem'
            item['xiaoquID'] = xiaoquID
            try:
                item['url'] = house.xpath('div[@class="title"]/a/@href').extract()[0]
            except Exception as e:
                item['url'] = 'error'

            try:
                item['title'] = house.xpath('div[@class="title"]/a/text()').extract()[0]
            except Exception as e:
                item['title'] = 'error'

            try:
                item['id'] = house.xpath('div[@class="title"]/a/@data-housecode').extract()[0]
            except Exception as e:
                item['id'] = 'error'

            try:
                item['xiaoqu'] = house.xpath('div[@class="flood"]/div/a/text()').extract()[0]
            except Exception as e:
                item['xiaoqu'] = 'error'

            try:
                item['addr'] = house.xpath('div[@class="flood"]/div/a/text()').extract()[1]
            except Exception as e:
                item['addr'] = 'error'

            try:
                address = house.xpath('div[@class="address"]/div[@class="houseInfo"]/text()').extract()[0].split('|')
                if len(address) >= 1:
                    item['layout'] = address[0]
                if len(address) >= 2:
                    item['area'] = address[1]
                if len(address) >= 3:
                    item['direction'] = address[2]
                if len(address) >= 4:
                    item['style'] = address[3]
                if len(address) >= 5:
                    item['floor'] = address[4]
                if len(address) >= 6:
                    item['year'] = address[5]
                if len(address) >= 7:
                    item['houseType'] = address[6]
            except Exception as e:
                item['layout'] = 'error'
                item['area'] = 'error'
                item['direction'] = 'error'
                item['style'] = 'error'
                item['floor'] = 'error'
                item['year'] = 'error'
                item['houseType'] = 'error'

            try:
                tmp = house.xpath('div[@class="followInfo"]/text()').extract()[0].split('/')
                if len(tmp) >= 1:
                    item['care'] = tmp[0]
                if len(tmp) >= 2:
                    item['publish'] = tmp[1]
            except Exception as e:
                item['care'] = 'error'
                item['publish'] = 'error'
            try:
                item['price'] = house.xpath('div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract()[0]
            except Exception as e:
                item['price'] = 'error'
            try:
                item['unitPrice'] = house.xpath('div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()').extract()[0]
            except Exception as e:
                item['unitPrice'] = 'error'

            yield item

    def parse_dealHouseItemFromListPage(self, response):
        url = response.url;
        # 定位 共找到 232 套广州成交房源 确认数量 如果小区 成交数量为0 会跳转到展示广州所有历史成交记录页面 则跳过
        try:
            dealNum = int(response.xpath('//div[@class="total fl"]/span/text()').extract()[0])
            if dealNum >10000:
                logger.info('%s this page is guangzhou total deal page'  % (url))
                return
            elif dealNum >30:
                index1 = url.find('pg')
                index2 = url.find('c', index1 + 2)
                before = url[0:index1 + 2]
                after = url[index2:]
                for a in range(2, dealNum/30 + 2, 1):
                    newurl = '%s%d%s' % (before, a, after)
                    yield Request(newurl, callback=self.parse_dealHouseItemFromListPage)
                    # print newurl
            elif dealNum == 0:
                logger.info('%s this xiaoqu 0 house is dealed' % (url))
                return
        except Exception as e:
            logger.error('%s get dealNum error' % (url))
            return

        tmp1 = url.split('/')[-2]
        xiaoquID = tmp1[tmp1.find('c'):]
        # 开始解析房源信息
        item = DealHouseItem()
        houses = response.xpath('//li/div[@class="info"]')

        for house in houses:
            item['type'] = 'DealHouseItem'
            item['xiaoquID'] = xiaoquID
            try:
                item['url'] = house.xpath('div[@class="title"]/a/@href').extract()[0]
            except Exception as e:
                item['url'] = 'error'

            try:
                item['id'] = item['url'].split('/')[-1][:-5]
            except Exception as e:
                item['id'] = 'error'

            try:
                item['listPrice'] = house.xpath('div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[1]/text()').extract()[0]
            except Exception as e:
                item['listPrice'] = 'error'

            try:
                item['dealDays'] = house.xpath('div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"]/span[2]/text()').extract()[0]
            except Exception as e:
                item['dealDays'] = 'error'

            try:
                item['dealDate'] = house.xpath('div[@class="address"]/div[@class="dealDate"]/text()').extract()[0]
            except Exception as e:
                item['dealDate'] = 'error'

            try:
                item['dealPrice'] = house.xpath('div[@class="address"]/div[@class="totalPrice"]/span/text()').extract()[0]
            except Exception as e:
                item['dealPrice'] = 'error'

            try:
                item['averagePrice'] = house.xpath('div[@class="flood"]/div[@class="unitPrice"]/span/text()').extract()[0]
            except Exception as e:
                item['averagePrice'] = 'error'
            yield item




