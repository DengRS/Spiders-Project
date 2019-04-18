import requests
from requests.exceptions import RequestException
from fake_useragent import FakeUserAgent
from retry import retry
import logging
import json
import csv
import os
from MeiTuan_Spider.settings import data_path

class Log(object):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s  %(levelname)s]: %(message)s')

    @classmethod
    def log(cls, file_log=False):
        if file_log:
            file_handler = logging.FileHandler(filename='MeiTuan.log')
            file_handler.setFormatter(cls.formatter)
            cls.logger.addHandler(file_handler)
        else:
            console_handler = logging.StreamHandler()
            console_handler.formatter = cls.formatter
            cls.logger.addHandler(console_handler)
        return cls.logger


logger = Log.log()


class Spider(object):
    ua = FakeUserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
    }

    @retry((RequestException, ValueError), tries=3, delay=5, logger=logger)
    def _crawl(self, url, headers={}, plain=None):
        if headers and isinstance(headers, dict):
            Spider.headers.update(headers)
        response = requests.get(url, headers=self.headers, timeout=25)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            if plain != 'text':
                return response.json()
            else:
                return response.text
        else:
            raise ValueError('状态码错误')

    def crawl(self, *args, **kwargs):
        obj = None
        if args:
            url = args[0]
        else:
            url = kwargs.get('url')
        try:
            obj = self._crawl(*args, **kwargs)
            logger.info('请求成功[√]: {}'.format(url))
        except (RequestException, ValueError) as error:
            logger.error('请求失败[×]: {}'.format(url))
            logger.error(error)
        finally:
            return obj


class Tool(object):
    def __init__(self):
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        self._path = data_path + '/'

    def save_to_json(self, file, data, mode='w'):
        if isinstance(data, dict):
            logger.info('开始保存数据......')
            with open(file, mode, encoding='utf-8') as fp:
                json.dump(data, fp, ensure_ascii=False, indent=8)
            logger.info('数据保存成功 √')
        else:
            logger.error('数据保存失败 ×')

    def save_to_csv(self, headers, file, data, mode='w'):
        if isinstance(data, list) and isinstance(headers, list):
            logger.info('开始保存数据......')
            with open(self._path + file, mode, encoding='utf-8') as fp:
                csv_file = csv.DictWriter(fp, fieldnames=headers)
                csv_file.writeheader()
                csv_file.writerows(data)
                logger.info('数据保存成功 √')
        else:
            logger.error('数据保存失败 ×')

    def read_from_json(self, file):
        with open(file, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        return data


if __name__ == '__main__':
    tool = Tool()
