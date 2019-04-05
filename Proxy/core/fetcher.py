from core.crawl import *
from website_spiders import *
import random
from core.database import RedisDataBase
from core.utils import delay, wait

class Fetcher():
    """获取代理IP模块"""
    max_page = 2

    def __init__(self):
        self.redis = RedisDataBase()

    def run_get_page(self, site):
        url = site.url
        html = crawl(url=url)
        if html:
            self.max_page = min(random.randrange(25, 50), site.get_page(html))
        delay()

    def run_parser(self, site):
        for num in range(1, 1+self.max_page):
            url = site.url + str(num)
            html = crawl(url=url)
            if html:
                for proxy in site.parser(html):
                    self.redis.add(proxy.get('core'))
            delay()

    @wait(60 * 60)
    def run(self):
        # 半天采集一次
        for site in WeSites:
            site = eval(site)
            self.run_get_page(site)
            self.run_parser(site)
