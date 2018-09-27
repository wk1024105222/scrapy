# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import uuid

from picture.dbpool import pool


class DividendPipeline(object):
    def __init__(self):
        self.con = pool.connection()
    def process_item(self, item, spider):
        cursor = self.con.cursor()
        sql = "insert into stockdevidend(uuid,date1,year,stockDividend,transfeShares,dividendPayout,date2,date3,date4,code) " \
              "value('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
              (uuid.uuid1(),item['date1'],item['year'],item['stockDividend'],item['transfeShares'],item['dividendPayout'],item['date2'],item['date3'],item['date4'],item['code'])
        try:
            # print sql
            cursor.execute(sql)
            self.con.commit()
        except Exception as e:
            logging.info(sql)
            logging.info(e)

        return item

    def spider_closed(self, spider):
        self.con.close()



