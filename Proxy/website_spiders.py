from lxml import etree
from re import compile, findall

WeSites = []

# 爬虫类的扩展
# 示例
"""
class Website_xxx(metaclass=CrawlerMeta):
    url = None
    
    @classmethod
    def get_page(cls, html):
        return None
        
    @classmethod
    def parser(cls, html):
        yield {
            'core': None
        }
"""

class CrawlerMeta(type):
    """收集爬虫类"""
    def __new__(cls, name, bases, attrs):
        if 'Website_' not in name:
            raise NameError(f'the [{name}] crawler named error')
        if not ('get_page' in attrs.keys() and 'parser' in attrs.keys() and 'url' in attrs.keys()):
            raise AttributeError(f'the [{name}] crawler must be has "get_page"、"parser" and "url" attribute')
        WeSites.append(name)
        return type.__new__(cls, name, bases, attrs)


class Website_XiCi(metaclass=CrawlerMeta):
    # 西刺代理
    url = 'https://www.xicidaili.com/nn/'

    @classmethod
    def get_page(cls, html):
        content = etree.HTML(html)
        max_page = content.xpath('//*[@class="pagination"]/a[last()-1]/text()')
        return int(max_page[0])

    @classmethod
    def parser(cls, html):
        content = etree.HTML(html)
        for tr in content.xpath('//*[@id="ip_list"]//tr[position()>1]'):
            ip = tr.xpath('./td[position()=2]/text()')[0]
            port = tr.xpath('./td[position()=3]/text()')[0]
            type = tr.xpath('./td[position()=6]/text()')[0]
            yield {
                'core': f'{type.lower()}://{ip}:{port}'
            }

class Website_KuaiDaiLi(metaclass=CrawlerMeta):
    # 快代理
    url = 'https://www.kuaidaili.com/free/inha/'

    @classmethod
    def get_page(cls, html):
        content = etree.HTML(html)
        max_page = content.xpath('//*[@id="listnav"]//li[last()-1]/a/text()')
        return int(max_page[0])

    @classmethod
    def parser(cls, html):
        content = etree.HTML(html)
        trs = content.xpath('//*[@id="list"]/table//tr[position()>1]')
        for tr in trs:
            ip = tr.xpath('./td[@data-title="IP"]/text()')[0]
            port = tr.xpath('./td[@data-title="PORT"]/text()')[0]
            type = tr.xpath('./td[@data-title="类型"]/text()')[0]
            yield {
                'core': f'{type.lower()}://{ip}:{port}'
            }




