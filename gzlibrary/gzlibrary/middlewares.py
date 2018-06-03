# -*- coding: utf-8 -*-
import random
import base64

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        #print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

PROXIES = [
    {'ip_port': '120.79.161.105:8888', 'user_pass': ''},
    # {'ip_port': '14.118.255.153:6666', 'user_pass': ''},
    # {'ip_port': '113.240.226.164:8080', 'user_pass': ''},
    # {'ip_port': '106.56.102.65:8070', 'user_pass': ''},
    # {'ip_port': '222.185.137.118:6666', 'user_pass': ''},
    # {'ip_port': '112.228.172.122:8118', 'user_pass': ''},
    # {'ip_port': '60.214.118.170:6300', 'user_pass': ''},
    # {'ip_port': '115.194.108.47:8118', 'user_pass': ''},
    # {'ip_port': '61.135.217.7:80:', 'user_pass': ''},
    # {'ip_port': '122.114.31.177:808:', 'user_pass': ''},
    # {'ip_port': '27.197.53.157:8118', 'user_pass': ''},
    # {'ip_port': '221.228.17.172:8181', 'user_pass': ''}
]

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

