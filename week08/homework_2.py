'''
自定义一个 python 函数，实现 map() 函数的功能
'''

def custom_map(func, iterable):
    return (func(i) for i in iterable)


def squre(x):
    return x**2
 
res = custom_map(squre, [1, 2, 3])
print(next(res))
print(list(res))