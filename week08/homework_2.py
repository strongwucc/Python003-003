'''
自定义一个 python 函数，实现 map() 函数的功能
'''

'''
自定义 map
'''


def custom_map(func, *args):
    return (func(*arg) for arg in zip(*args))


'''
平方计算
'''


def square(*args):
    return tuple(i**2 for i in args) if len(args) > 1 else args[0]**2


if __name__ == "__main__":
    iter = custom_map(square, [1, 2, 3], [4, 5, 6, 7])
    # iter = map(square, [1, 2, 3], [4, 5, 6, 7])
    # iter = custom_map(square, [1, 2, 3])
    print(list(iter))
