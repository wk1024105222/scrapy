# -*- coding: utf-8 -*-

from scrapy import Spider, Request
import json
from zolnotebook.items import ZolnotebookItem

# 已完成任务缓存
done={}
lines = open('zolnotebookV1.0.json').readlines()
for line in lines:
    a = json.loads(line)
    if a.has_key('url'):
        id = a['url'].encode('utf-8').split('/')[-2]
        done[id]=1

class ZolNoteBookCrawlerSpider(Spider):

    name = 'zolnotebook_spider'
    allowed_domains = ['http://detail.zol.com.cn/']
    #V2.0 按内存大小
    start_urls =  \
                    ['http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s6648_1_2_0_'+str(i)+'.html' for i in range(1, 3,1) ]+\
                    ['http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s5730_1_2_0_'+str(i)+'.html' for i in range(1,14,1) ]+\
                    ['http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s4108_1_2_0_'+str(i)+'.html' for i in range(1,63,1) ]+\
                    ['http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s2192_1_2_0_'+str(i)+'.html' for i in range(1,105,1)]+\
                    [ 'http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s108_1_2_0_'+str(i)+'.html' for i in range(1,105,1)]
    #V1.0 按上市时间
    # start_urls =  \
    #                 [ 'http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s7236_1_2_0_'+str(i)+'.html' for i in range(1, 8,1)]+\
    #                 [ 'http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s6974_1_2_0_'+str(i)+'.html' for i in range(1,19,1)]+\
    #                 [ 'http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s6456_1_2_0_'+str(i)+'.html' for i in range(1,23,1)]+\
    #                 [ 'http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s6316_1_2_0_'+str(i)+'.html' for i in range(1,32,1)]+\
    #                 [ 'http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s6133_1_2_0_'+str(i)+'.html' for i in range(1,24,1)]+\
    #                 [ 'http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_s5719_1_2_0_'+str(i)+'.html' for i in range(1,76,1)]


    def parse(self, response):
        ids =  response.xpath('//li[@data-follow-id]/@data-follow-id').extract()
        prices = response.xpath('//b[@class="price-type"]/text()').extract()
        length = len(ids)

        for a in ids:
            id = a[1:]
            if done.has_key(id):
                continue
            page = int(id) /1000+1
            url = 'http://detail.zol.com.cn/'+str(page)+'/'+str(id)+'/param.shtml'
            # print  url
            yield Request(url, callback=self.parse_item, dont_filter=True)

        item = ZolnotebookItem()
        map = {}
        if len(prices) == length:

            for index in range(0, length, 1):
                map['id'] = ids[index][1:]
                map['price'] = prices[index]
                item['param']=map
                yield item
        else:
            print response.url,'价格数量与ID数量不一致'

    def parse_item(self, response):
        item = ZolnotebookItem()

        num = [tmp.split('_')[1] for tmp in response.xpath('//span[@class="param-name"]/@id').extract()]+\
              [tmp.split('_')[1] for tmp in response.xpath('//span[@class="param-name param-explain"]/@id').extract()]
        map = {}
        # file_object = open(r'thefile.txt', 'w')
        for i in num:
            name = response.xpath('//span[@id="newPmName_'+i+'"]/text()').extract()
            name_len=len(name)
            if name_len == 0:
                name = ''
            else:
                if name_len == 1:
                    name = name[0]
                else:
                    name = ' '.join(name)

            value = response.xpath('//span[@id="newPmVal_'+i+'"]/text()').extract()+ response.xpath('//span[@id="newPmVal_'+i+'"]/a/text()').extract()
            value_len = len(value)
            if value_len == 0:
                value = ''
            else:
                if value_len == 1:
                    value = value[0]
                else:
                    value = '|'.join(value)

            a = name.encode('utf-8')
            b = value.encode('utf-8')
            # file_object.write(a+'=====')
            # file_object.write(b+'\n')
            map[a] = b.replace('\r','').replace('\n','').replace(',','')
            # map[name] = value.encode("utf-8").replace('\r','').replace('\n','').replace(',','')

        try:
            name = response.xpath('//a[@class="back_home_btn"]/span/text()').extract()[0][2:-2]
        except Exception as e:
            name='error'

        map['url'] = response.url
        map['name'] = name
        item['param']=map
        # file_object.write(response.url+'\n')
        # file_object.write(item['name'].encode('utf-8')+'\n')
        # print response.url, '================================================================================'
        # file_object.close( )
        return item
