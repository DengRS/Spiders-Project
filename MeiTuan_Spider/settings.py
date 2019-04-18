import time
import random
import os

delay_s = lambda: time.sleep(random.randint(2,5))

delay = lambda x: time.sleep(x)

base_ciity_url = 'https://bj.meituan.com'

city_href_path = os.getcwd() + '/MeiTuan-City.json'

data_path = os.getcwd() + '/data'