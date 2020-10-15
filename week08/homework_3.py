'''
实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数
'''

import time
from functools import wraps


def timer(func):
    @wraps(func)
    def timing(*args, **kwargs):
        start_time = time.time()
        resp = func(*args, **kwargs)
        end_time = time.time()
        print(f'{func.__name__} excuted for {end_time - start_time:.3f}')
        return resp
    return timing


@timer
def test_func(limit):
    i = 0
    while i < limit:
        i += 1


if __name__ == "__main__":
    test_func(50000000)
