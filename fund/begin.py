__author__ = 'wkai'

from scrapy import cmdline
cmdline.execute("scrapy crawl fund_spider -o fund_spider.json".split())

