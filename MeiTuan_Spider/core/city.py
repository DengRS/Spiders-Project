from MeiTuan_Spider.core.utils import Spider, Tool
from MeiTuan_Spider.settings import city_href_path
from lxml import etree
from collections import defaultdict


class CityLinks(object):
    # 城市链接
    def __init__(self):
        self.spider = Spider()
        self.file = Tool()
        self.data = defaultdict(dict)
        self.url = 'https://www.meituan.com/changecity/'

    def get_page(self):
        html = self.spider.crawl(url=self.url, plain='text')
        content = etree.HTML(html)
        divs = content.xpath('//*[@class="alphabet-city-area"]/div')
        if divs:
            for div in divs:
                city_label = div.xpath('./span[@class="city-label"]/text()')[0]
                cities = div.xpath('./span[@class="cities"]/a')
                for city in cities:
                    href = city.xpath('./@href')[0]
                    name = city.xpath('./text()')[0]
                    self.data[city_label].update({name: 'https:' + href})

        self.file.save_to_json(city_href_path, self.data)


if __name__ == '__main__':
    city = CityLinks()
    city.get_page()
