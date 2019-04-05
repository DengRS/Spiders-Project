from core.tester import Tester
from core.fetcher import Fetcher
from core.database import RedisDataBase
from core.utils import *
from core.proxy_api import app
from multiprocessing import Process, Queue


queue = Queue()

class Scheduler(object):
    test = Tester()
    fetch = Fetcher()
    redis = RedisDataBase()

    def _test(self, queue):
        while True:
            if not self.redis.is_empty:
                print(getTime('测试代理模块开始启动'))
                self.test.run()
            else:
                print(getTime('代理池枯竭, 测试代理模块被迫进入休眠状态'))
                queue.put('True')
                delay(60 * 60)

    def _fetch(self, queue, flag=False):
        while True:
            if not queue.empty():
                flag = queue.get()
            if flag:
                flag = False
                print(getTime('代理池枯竭, 获取代理模块被迫启动'))
                self.fetch.run()
            if times() in [6, 18]:
                # 设置时间为6、18 时启动
                print(getTime('获取代理模块开始启动'))
                self.fetch.run()
                print(getTime('获取完成, 获取代理模块进入休眠状态'))
    def _app(self):
        app.run(host='0.0.0.0')

    def all_run(self):
        print(getTime('代理池开始运行......'))
        tester = Process(target=self._test, args=(queue,))
        tester.start()
        fetcher = Process(target=self._fetch, args=(queue,))
        fetcher.start()
        app = Process(target=self._app)
        app.start()

if __name__ == '__main__':
    schedule = Scheduler()
    schedule.all_run()


