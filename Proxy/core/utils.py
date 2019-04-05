import time, random

def getTime(info: str):
    times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return f'[{times}] INFO: {info}'

def delay(start: int=2, end: int=None):
    if end != None:
        time.sleep(random.randint(start, end))
    else:
        time.sleep(start)

def times():
    return int(time.strftime('%H'))

def wait(delay: int=10):
    def wrap(func):
        def function(*args, **kwargs):
            func(*args, **kwargs)
            time.sleep(delay)
        return function
    return wrap
