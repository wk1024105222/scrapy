# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from gzlibrary.dbpool import pool

class GzlibraryPipeline(object):

    def __init__(self):
        self.con = con = pool.connection()
        self.file = codecs.open('gzlibrary_spider.json', 'a', encoding='utf-8')
        self.error = codecs.open('error.log', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        try:
            cursor =self.con.cursor()
            cursor.execute("insert into gzlibbookinfo(id,name,author,press,pubdate) values('%s','%s','%s','%s','%s') " % (item['id'] ,item['name'].replace("'","''") ,item['author'].replace("'","''") ,item['press'] ,item['pubdate']))
            self.con.commit()
        except Exception as e:
            self.error.write(line)
            self.error.write(e)
        return item

    def spider_closed(self, spider):
        self.con.close()
        self.file.close()
        self.error.close()
