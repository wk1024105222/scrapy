__author__ = 'wkai'

from scrapy import cmdline

# cmdline.execute("scrapy crawl gzlibrary_spider -o gzlibrary_spider.json".split())

cmdline.execute("scrapy crawl gzlibrary_spider".split())