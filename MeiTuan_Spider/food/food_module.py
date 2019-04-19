from MeiTuan_Spider.core.utils import logger, Spider, Tool
from MeiTuan_Spider.core.get_url import ConstructURL
from MeiTuan_Spider.core.cookies import single_cookie
from MeiTuan_Spider.core.city import CityLinks
from MeiTuan_Spider.settings import *
from collections import defaultdict
import os


class FoodData(object):
    headers = ['店名', '地址', '平均得分', '评论数', '图片']
    file_path = '{}.csv'

    def __init__(self):
        self.spider = Spider()
        self.file = Tool()
        self.city = CityLinks()
        self.data = defaultdict(list)
        self.url = ConstructURL
        self._href = '{}/meishi/pn{}/'
        self.max_page = 67

    def single_city(self, city, city_url):
        # 抓取单个城市的美食数据
        for page in range(1, self.max_page+1):
            logger.info('正在抓取 [{}] -- 第{}页数据'.format(city, page))
            url = self.url(self._href.format(city_url, page), self._href.format(city_url, page-1), city, page, single_cookie())
            food_data = self.spider.crawl(url=str(url))
            if food_data:
                _data = food_data.get('data')
                if _data:
                    for data in _data.get('poiInfos'):
                        self.data['data'].append({
                            '店名': data.get('title'),
                            '地址': data.get('address'),
                            '平均得分': data.get('avgScore'),
                            '评论数': data.get('allCommentNum'),
                            '图片': data.get('frontImg'),
                        })
            delay_s()
        self.file.save_to_csv(self.headers, self.file_path.format(city), self.data['data'], mode='a+')
        self.data.clear()

    def all_city(self):
        if not os.path.exists(city_href_path):
            self.city.get_page()
        delay_s()
        data = self.file.read_from_json(city_href_path)
        for value in data.values():
            for k, v in value.items():
                self.single_city(k, v)
                delay(15)

    def run(self):
        all_data = False
        if all_data:
            self.all_city()
        else:
            city = input('请输入要抓取的城市[美食]: ')
            self.single_city(city, base_ciity_url)


if __name__ == '__main__':
    food = FoodData()
    food.run()




