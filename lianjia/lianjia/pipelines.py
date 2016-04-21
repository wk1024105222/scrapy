# -*- coding: utf-8 -*-
from scrapy import signals
import json
import codecs


class LianjiaPipeline(object):
    def __init__(self):
        self.file = codecs.open('lianjia.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()