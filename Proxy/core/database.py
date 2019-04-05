from redis import StrictRedis
from settings import *
from core.utils import *


class RedisDataBase(object):
    """Redis 数据库"""

    def __init__(self):
        self.client = StrictRedis(host=HOST, port=PORT, password=PWD, db=DB)

    def exists(self, proxy: str):
        # 判断代理是否存在
        if self.client.zscore(KEY, proxy):
            return True
        return False

    def add(self, proxy: str):
        # 添加代理
        if not self.exists(proxy):
            self.client.zadd(KEY, {proxy: INIT_SCORE})

    @property
    def total(self):
        # 数据库代理池总量
        return int(self.client.zcard(KEY))

    @property
    def is_empty(self):
        # True: 代理池为空
        # False: 代理池非空
        return self.total == 0

    def take(self, start: int, end: int):
        # 测试代理
        return self.client.zrange(KEY, start, end)

    def change(self, proxy: str, status: bool):
        # 代理变更
        # status: True: 成功, False: 失败
        if status:
            self.client.zadd(KEY, {proxy: SUCCESS_SCORE})
            print(getTime(f'代理测试成功 √ [{int(self.client.zscore(KEY, proxy))}]: {proxy}'))
        else:
            self.client.zincrby(KEY, -1, proxy)
            score = self.client.zscore(KEY, proxy)
            if score == 0:
                print(getTime(f'代理已失效 × [移除]: {proxy}'))
                return self.client.zrem(KEY, proxy)
            print(getTime(f'代理测试失败 × [{int(self.client.zscore(KEY, proxy))}]: {proxy}'))

    @property
    def get_proxies(self):
        success_proxies = self.client.zrangebyscore(KEY, SUCCESS_SCORE, SUCCESS_SCORE)
        if len(success_proxies) > 0:
            return {
                'proxies': [proxy.decode() for proxy in success_proxies if isinstance(proxy, bytes)]
            }
        else:
            proxies = self.client.zrangebyscore(KEY, INIT_SCORE, SUCCESS_SCORE)
            if len(proxies) > 0:
                return {
                    'proxies': [proxy.decode() for proxy in proxies if isinstance(proxy, bytes)]
                }
            else:
                return None