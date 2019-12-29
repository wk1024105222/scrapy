# -*- coding: utf-8 -*-
import logging
from pybloom import BloomFilter

from scrapy import Spider, Request
from lianjia.items import SchoolItem, RecruitStudentsItem

logger = logging.getLogger('fangtianxiaschool_spider')
f = BloomFilter(capacity=10000, error_rate=0.00001)

class fangtianxiaschool_spider(Spider):
    '''
        根据房天下小学列表 爬取小学信息 对口中学 招生范围 地址GPS 等
    '''
    name = 'fangtianxiaschool_spider'
    allowed_domains = ['gz.esf.fang.com']
    start_urls = ['https://gz.esf.fang.com/school/i3%s/' % (i) for i in range(1,16,1)]
    # start_urls = ['https://gz.esf.fang.com/school/i31/' ]

    def parse(self, response):
        # 获取当前页面学校url
        schoolUrls = response.xpath('//p[@class="title"]/a/@href').extract()
        for url in schoolUrls:
            if url in f:
                logger.warn('%s has been visited' % (url))
                continue
            else:
                f.add(url)
                yield Request('https://gz.esf.fang.com%s' % (url), callback=self.parse_schoolItemFromDetailPage,dont_filter=True)
        #     break
        # yield Request('https://gz.esf.fang.com/school/257.htm', callback=self.parse_schoolItemFromDetailPage,
        #               dont_filter=True)

        # yield Request('https://gz.esf.fang.com/school/262/profile/#profile' ,
        #               callback=self.parse_recruitStudentsItemFromDetailPage,
        #               dont_filter=True)

    def parse_schoolItemFromDetailPage(self, response):

        item = SchoolItem()
        item['url'] = response.url
        item['type'] = 'SchoolItem'
        item['id'] = response.url.split('/')[-1][:-4]
        try:
            item['name'] = response.xpath('//p[@class="schoolname"]/span[@class="title"]/text()').extract()[0]
        except Exception as e:
            item['name'] = 'error'

        try:
            q = response.xpath('//p[@class="schoolname"]/span[@class="info gray9 ml10"]/text()').extract()[0].strip()
            p =q[1:-1]
            info = p.split('|')
            if len(info) == 3:
                item['primaryMiddle'] = info[0]
                item['rank'] =info[1]
                index = info[2].find(u'别名')
                item['alias']= info[2].strip()[index+3:]
                item['statePrivare']=info[2].strip()[0:index]
        except Exception as e:
            item['primaryMiddle'] = 'error'
            item['rank'] = 'error'
            item['alias'] = 'error'
            item['statePrivare'] = 'error'

        infoTags = response.xpath('//div[@class="info floatr"]/ul/li')
        for tag in infoTags:
            names = tag.xpath('span[@class="gray6"]/text()').extract()
            name = u''
            if names == None or len(names)==0:
                continue
            else:
                name = names[0]
            if name == None:
                continue
            elif name == u'学校地址：':
                try:
                    item['addr'] = tag.xpath('text()').extract()[0]
                except Exception as e:
                    item['addr'] = 'error'
            elif name == u'学校特色：':
                try:
                    item['featureTag'] = tag.xpath('span[@class="pr5"]/text()').extract()
                except Exception as e:
                    item['featureTag'] = 'error'
            elif name == u'学校电话：':
                try:
                    item['tel'] = tag.xpath('text()').extract()[0]
                except Exception as e:
                    item['tel'] = 'error'

            elif name == u'升学情况：':
                try:
                    toSchoolNames = tag.xpath('p/a[@class="pr5 blue"]/text()').extract()
                    item['toSchool'] = toSchoolNames
                except Exception as e:
                    item['toSchool'] = 'error'

                try:
                    toSchoolUrls = tag.xpath('p/a[@class="pr5 blue"]/@href').extract()
                    for url in toSchoolUrls:
                        if url in f:
                            logger.warn('%s has been visited' % (url))
                            continue
                        else:
                            f.add(url)
                            yield Request('https://gz.esf.fang.com%s' % (url),
                                          callback=self.parse_schoolItemFromDetailPage, dont_filter=True)
                except Exception as e:
                    logger.error('%s get toSchool Error ' % (response.url))

        url = 'https://gz.esf.fang.com/school/%s/profile/#profile' % (item['id'])
        if url in f:
            logger.warn('%s has been visited' % (url))
        else:
            f.add(url)
            yield Request(url, callback=self.parse_recruitStudentsItemFromDetailPage,dont_filter=True)

        yield item

    def parse_recruitStudentsItemFromDetailPage(self, response):
        item = RecruitStudentsItem()
        item['id'] = response.url.split('/')[4]
        item['type'] = 'RecruitStudentsItem'
        item['url'] = response.url

        tags = response.xpath('//div[@class="profile"]/dl')

        for tag in tags:
            tagName = tag.xpath('dt/text()').extract()[0]
            str = ""
            x = tag.xpath('dd[1]/p[@style="display:none "]/text()').extract()
            if x != None and len(x)>0:
                for m in x:
                    str += m + '\r\n'
            else:
                x = tag.xpath('dd[1]/p[@style="display:none"]/text()').extract()
                if x != None and len(x)>0:
                    for m in x:
                        str += m + '\r\n'
                else:
                    x = tag.xpath('dd[1]/p[@style="display:"]/text()').extract()

                    if x != None and len(x)>0:
                        for m in x:
                            str += m + '\r\n'
                    else:
                        str = 'error'
            if tagName==u'招生简章':
                item['brochure'] =str
            elif  tagName==u'学校介绍':
                item['introduce']=str
            elif tagName == u'招生范围':
                item['scope']=str
            elif tagName == u'入学条件':
                item['require']=str
            elif tagName== u'学校特色描述':
                item['feature']=str
        yield item