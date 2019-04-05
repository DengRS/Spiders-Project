from core.crawl import async_crawl
from settings import TEST_URL, STEP
from core.database import RedisDataBase
from core.utils import *
import asyncio


class Tester(object):
    def __init__(self):
        self.redis = RedisDataBase()

    async def _run(self, proxy):
        if isinstance(proxy, bytes):
            proxy = proxy.decode()
        bool = await async_crawl(url=TEST_URL, proxy=proxy)
        self.redis.change(proxy, bool)

    @wait(60 * 60)
    def run(self):
        # 一个小时测试一次
        count = self.redis.total
        print(getTime(f'当前代理IP总量: {count}'))
        for num in range(0, count, STEP-1):
            start, end = num, min(num+STEP, count)
            proxies = self.redis.take(start, end)
            tasks = [self._run(proxy) for proxy in proxies]
            if len(tasks) != 0:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncio.wait(tasks))
                delay(5, 7)
        print(getTime(f'删除无效代理 × {[abs(self.redis.total - count)]}'))
        print(getTime('测试完成, 测试代理模块进入休眠状态'))
