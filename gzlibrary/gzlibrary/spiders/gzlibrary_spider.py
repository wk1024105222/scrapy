# -*- coding: utf-8 -*-
import logging
from scrapy import Spider
from gzlibrary.items import BookItem
from gzlibrary.dbpool import pool

logging.basicConfig(level=logging.ERROR,
                filemode='a',
                format='%(asctime)s %(thread)d [line:%(lineno)d] [%(threadName)s] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='gzlibrary_spider.log')
#从数据库里取10个 未下载的页面
con = pool.connection()
cursor = con.cursor()
cursor.execute("select url from (select url from gzlibraryurl where DOWNFLAG='0' order by booktype,pagenum) t where rownum<11")
allBookPages = []
for url in cursor.fetchall():
    allBookPages.append(url[0])
con.close()

class GZLibrarySpider(Spider):
    name = 'gzlibrary_spider'
    allowed_domains = ['http://opac.gzlib.gov.cn/opac']
    start_urls = allBookPages
    # start_urls = ['http://opac.gzlib.gov.cn/opac/search?q=TP&searchType=standard&isFacet=false&view=simple&searchWay=class&booktype=1&rows=10&sortWay=score&sortOrder=desc&libcode=GT&searchWay0=marc&logical0=AND&page=5']

    def parse(self, response):
        '''
        从每个页面中获取1000本书的信息 以及 发起馆藏信息查询
        :param response:
        :return:
        '''

        tmp1 = response.url.index('search?q=')+9
        tmp2 = response.url.index('&searchType')

        tmp3 = response.url.index('page=')+5

        name = 'html\\'+response.url[tmp1:tmp2]+response.url[tmp3:]+'.txt'

        file = open(name, 'w')
        file.write(response.body)
        file.close()

        books =  response.xpath('//div[@class="bookmeta"]')
        for book in books:
            item = BookItem()
            item['id'] = book.xpath('@bookrecno').extract()[0]


            item['name'] = book.xpath('div/span[@class="bookmetaTitle"]/a/text()').extract()[0].strip()

            item['author'] = book.xpath('div/a/text()').extract()[2].strip()
            item['press'] = book.xpath('div/a/text()').extract()[3].strip()
            item['pubdate'] = book.xpath('div/text()').extract()[6].strip()[5:].strip()

            yield item

        con = pool.connection()
        cursor = con.cursor()
        cursor.execute("update gzlibraryurl set downflag=%d where url='%s'" % (1,response.url))
        con.commit()
        con.close()
        # yield Request('http://opac.gzlib.gov.cn/opac/book/%s' % (item['id']), callback=self.parse_item,dont_filter=True)

    def parse_item(self, response):
        print response.url
        # item = DagaierItem()
        # item['url']=response.url
        # item['name'] =  response.xpath('//h4/text()').extract()[0]
        # item['id'] = response.url.split('/')[-1]
        #
        #
        # urls = response.xpath('//div[@class="tpc_content do_not_catch"]/input/@src').extract()
        # if len(urls) == 0:
        #     urls = response.xpath('//p[@align="center"]/input/@src').extract()
        # item['pictures'] = urls
        # return item
        pass







