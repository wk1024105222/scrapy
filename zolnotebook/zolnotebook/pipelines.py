# -*- coding: utf-8 -*-

import json
import codecs

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ZolnotebookPipeline(object):

    def __init__(self):
        self.file = codecs.open('zolnotebook.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        # file_object = open(r'thefile.txt', 'w')
        # file_object.write(item['html'])
        # file_object.close( )
        # item['html']=''
        line = json.dumps(item['param'], ensure_ascii=True) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
