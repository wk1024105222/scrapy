# -*- coding: utf-8 -*-
from scrapy import signals
import codecs
import json
from lianjia.dbpool import pool


class LianjiaPipeline(object):
    def __init__(self):
        self.file = codecs.open('lianjia.json', 'a', encoding='utf-8')

        self.con = con = pool.connection()
        # self.file = codecs.open('gzlibrary_spider.json', 'a', encoding='utf-8')
        self.error = codecs.open('error.log', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)

        try:
            cursor =self.con.cursor()
            sql = ''
            if item['type']=='jbgk':
                sql = "INSERT INTO fund_baseinfo VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') " % (item['code'],
                                item['fullName'],
                                item['name'],
                                item['type'],
                                item['issueDate'],
                                item['listDate'],
                                item['company'],
                                item['manager'],
                                item['bank'],
                                item['bonus'],
                                item['manageRate'],
                                item['trusteeshipRate']
                                )
                cursor.execute(sql)
                cursor.execute("update fund_dataurl set flag='1' where url ='%s' " % (item['url']))
            self.con.commit()
        except Exception as e:
            cursor.execute("update fund_dataurl set flag='2' where url ='%s' " % (item['url']))
            self.con.commit()
            self.error.write(sql)
            #self.error.write(item)
            self.error.write(e)
        return item

    def spider_closed(self, spider):
        self.file.close()
        self.con.close()
        self.error.close()