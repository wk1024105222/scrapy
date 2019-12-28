__author__ = 'wkai'

from scrapy import cmdline
import time

cmd = "scrapy crawl lianjiahouse_spider3 -o lianjiaxiaoqu_spider_%s.json" % (time.strftime("%Y%m%d%H%M%S", time.localtime()))

cmdline.execute(cmd.split())