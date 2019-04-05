import asyncio, ssl
from aiohttp import ClientSession, TCPConnector
from aiohttp.client_exceptions import ClientHttpProxyError, ClientConnectionError, ClientError
import requests
from requests.exceptions import RequestException
from fake_useragent import FakeUserAgent
from core.utils import *


ua = FakeUserAgent()

class Crawler(object):
    """获取模块"""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
        'User-Agent': ua.random,
    }

    @classmethod
    async def async_crawl(cls, url: str, proxy: str=None):
        conn = TCPConnector(verify_ssl=False, limit=300)
        try:
            async with ClientSession(connector=conn, conn_timeout=20) as session:
                async with session.get(url, headers=cls.headers, timeout=10, proxy=proxy) as response:
                    if response.status in [200, 301, 302]:
                        return True
                    else:
                        raise ValueError(f'status: [{response.status}]; the status code is not 200')
        except (ClientHttpProxyError, asyncio.TimeoutError,
                ClientConnectionError, ClientError, ValueError, ssl.SSLError):
            return False

    @classmethod
    def crawl(cls, url: str, headers: dict={}):
        if headers:
            cls.headers.update(headers)
        try:
            response = requests.get(url=url, headers=cls.headers)
            if response.status_code == 200:
                print(getTime(f'请求成功 √: {url}'))
                response.encoding = response.apparent_encoding
                return response.text
            else:
                raise ValueError(f'status: [{response.status_code}]; the status code is not 200')
        except (RequestException, ValueError):
            print(getTime(f'请求失败 ×: {url}'))
            return None

def crawl(**kwargs):
    return Crawler.crawl(**kwargs)

def async_crawl(**kwargs):
    return Crawler.async_crawl(**kwargs)
