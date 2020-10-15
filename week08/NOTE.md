### 变量的赋值

##### 可变数据类型

- 列表 list
- 字典 dict

##### 不可变数据类型

- 整型 int
- 浮点型 float
- 字符串型 string
- 元组 tuple

> 变量赋值，可变数据类型传递的是对象的引用，不可变数据类型传递的是对象本身

> 如果变量是不可变数据类型，修改变量的值会开辟新的内存空间

> 如果变量是可变的数据类型，修改变量的值不会开辟新的内存空间，只对当前的内存空间进行修改，变量的引用地址不会变

> ==可变数据类型存在深拷贝、浅拷贝的问题==


### 序列的深浅拷贝

##### 序列的分类

- 容器序列：list、tuple、conllections.deque 等，能存放不同类型的数据
- 扁平序列：str、bytes、bytearray、memoryview（内存视图）、array.array 等，存放的是相同类型的数据，扁平序列只能容纳一种类型

##### 深浅拷贝示例

>深浅拷贝只对容器序列有效 

```
# list 和 切片操作会浅拷贝一个新的序列

list(obj)
obj[:]

# 使用 copy 进行深浅拷贝

import copy

copy.copy(obj)
copy.deepcopy(obj)

```

### 字典与扩展

##### 字典 key 的数据类型（不可变）

- 数字
- 字符串
- 元组

##### [collections](https://docs.python.org/zh-cn/3.7/library/collections.html)

- namedtuple 带命名的元组

```
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(10, y=20)
p.x + p.y
p[0] + p[1]
x, y = p
```

- Counter 计数器

```
from collections import Counter

mystring = ['a', 'b', 'c', 'c', 'c', 'a', 'b', 'd', 'e']
// 取得频率最高的前三个值
cnt = Counter(mystring)
cnt.most_common(3)
cnt['b']
```

- deque 双向队列

```
from collections import deque

d = deque('uvw')
d.append('xyz')
d.appendleft('rst')
```

### 变量作用域

Python 作用域遵循 LEGB 规则

LEGB 含义解释：

- L-Local(function); 函数内的名字空间
- E-Enclosing function locals; 外部嵌套函数的名字空间（例如closure）
- G-Global(module); 函数定义所在模块（文件）的名字空间
- B-Builtin(Python); Python 内置模块的名字空间

### 函数工具与高阶函数

##### 函数的可变长参数

一般可变长参数定义如下：

```
def func(*args, **kwargs):
    pass
    
// kwargs 获取关键字参数
// args 获取其他参数
```


##### 高阶函数

> 定义: 有参数是函数、返回值是函数

常见的高阶函数：

- map: map (函数， 序列) 将序列中每个值传入函数，处理完成返回为 map 对象
- reduce
- filter: filter (函数，序列)将序列中每个值传入函数，符合函数条件的返回为 filter 对象
- apply
- 偏函数

> apply 在Python2.3被移除，reduce 被放在functools包中 

> 推导式和生成器表达式可以替代 map 和 filter 函数

##### 偏函数

functools.partial:返回一个可调用的 partial 对象

使用方法:partial(func,*args,**kw)


```
from functools import partial

def add(x, y):
    return x + y
    
add_1 = partial(add, 1)

add_1(2) // 3
add_1(10) // 11
```
> func 是必须参数

> 至少需要一个 args 或 kw 参数

##### Lambda 表达式

- Lambda 只是表达式，不是所有的函数逻辑都能封装进去
- 实现简单函数的时候可以使用 Lambda 表达式替代
- 使用高阶函数的时候一般使用 Lambda 表达式

### 装饰器

#### 闭包


```
def line_conf(a, b):
    def line(x):
        return a*x+b
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5), line2(5))
```

```
def counter(start=0):
    def incr():
        nonlocal start
        start+=1
        return start
    return incr
```
> nonlocal 访问外部函数的局部变量

> 在函数外部已经定义了变量 start，在函数内部对该变量进行运算，运行时会遇到错误

> 主要是因为没有让解释器清楚变量是全局变量还是局部变量

#### 语法

```
def decorate(func):
    print('running in modlue')
    def inner(*args, **kwargs):
        # 增加逻辑
        return func(*args, **kwargs)
    return inner
    
@decorate
def func2():
    pass
  
# 真正执行的是 inner  
# 等效于下面
def func2():
    pass
    
func2 = decorate(func2)
```
> 装饰器在模块导入的时候自动运行

#### 带参数的装饰器

```
def decorate_out(*args1, **kwargs1):
    def decorate(func):
        def inner(*args2, **kwargs2):
            return func(*args2, **kwargs2)
        return inner
    return decorate


@decorate_out(4, 5, 6)
def func1(a, b, c):
    return a+b+c


# print(func1(1, 2, 3))
```

#### 内置装饰器

##### functools.wraps

```
from functools import wraps

def decorate_out(*args1, **kwargs1):
    def decorate(func):
        @wraps(func)
        def inner(*args2, **kwargs2):
            return func(*args2, **kwargs2)
        return inner
    return decorate


@decorate_out(4, 5, 6)
def func1(a, b, c):
    return a+b+c


# print(func1(1, 2, 3))
```
> @wraps 接受一个函数来进行装饰，并加入了复制函数名称、注释文档、参数列表等等的功能

##### functools.lru_cache

```
from functools import lru_cache
from time import time


@lru_cache(maxsize=2048)
def func1(counter=10000):
    total = 0
    while counter > 0:
        total += counter
        counter -= 1
    return total


start_time = time()
print(func1(100000000))
end_time = time()

print(f'1 run time is {end_time - start_time}')

start_time = time()
print(func1(100000000))
end_time = time()
print(f'2 run time is {end_time - start_time}')

```

#### 类装饰器

##### 带参数

```
class ClassDecorate(object):
    def __init__(self, *args, **kwargs):
        super(ClassDecorate, self).__init__()

    def __call__(self, func):
        def decoration_func(*args, **kwargs):
            return func(*args, **kwargs)
        return decoration_func

@ClassDecorate('wu',name='li')
def func1(args):
    return args

print(func1('lalalalla'))
```

##### 不带参数

```
class ClassDecorate(object):
    def __init__(self, func):
        self.func = func
        
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

@ClassDecorate
def func1():
    pass
```
##### 装饰类

```
def class_decorate(oldClass):

    class newClass(object):

        def __init__(self, *args, **kwargs):
            print(f'decorate is called：{args}，{kwargs}')
            self.wraps = oldClass(*args, **kwargs)

        def func(self, *args, **kwargs):
            print(f'decorate func is called：{args}, {kwargs}')
            return self.wraps.func(*args, **kwargs)

    return newClass

@class_decorate
class Kclass(object):
    
    def __init__(self, args):
        print(f'real class is called：{args}')

    def func(self, name):
        return f'real func is called：{name}'

kclss = Kclass('class_args')

print(kclss.func('func_args'))
```
> 装饰类中的某个方法

### 对象协议
> Duck Typing 的概念

#### 容器类型协议
- \_\_str__ 打印对象时，默认输出改方法的返回值
- \_\_getitem__、\_\_setitem__、\_\_delitem__ 字典索引操作
- \_\_iter__ 迭代器
- \_\_call__ 可调用对象协议

#### 比较大小的协议
- \_\_eq__
- \_\_gt__

#### 描述符协议和属性交互协议
- \_\_get__
- \_\_set__

#### 可哈希对象
- \_\_hash__

#### 上下文管理器

with 上下文表达式的用法

使用 \_\_enter__() 和 \_\_exit__() 实现上下文管理器


```
class MyContext(object):

    def __init__(self):
        pass

    def __enter__(self):
        print(f'__enter__ is called')

    def __exit__(self, exception_type, exception_value, traceback):
        print(f'__exit__ is called')
        print(exception_type.__class__)
        print(exception_value)
        print(dir(traceback))
        return True


with MyContext() as context:
    data = [1, 2, 3]
    print(data[4])
```

### 生成器

#### 可迭代对象和迭代器的区别

- Iterables（可迭代对象）：包含 \_\_getitem__() 或 \_\_iter__() 方法的容器对象
- Iterator（迭代器）：包含 next() 和 \_\_iter__() 方法
- Generator（生成器）：包含 yield 语句的函数

> 在函数中使用 yield 关键字，可以实现生成器

> 生成器可以让函数返回可迭代对象

> 字典进行插入操作后，字典迭代器会立即失效

> 列表尾部插入操作不会损坏指向当前元素的 List 迭代器，列表会自动变长

> 迭代器一旦耗尽，永久损坏

#### 利用 yield 实现生成器

```
def jumping_range(up_to):
    index = 0
    while index < up_to:
        jump = yield index
        print(f'jump is {jump}')
        if jump is None:
            jump = 1   # next() 或者 send(None)
        index += jump 
        print(f'index is {index}')

if __name__ == '__main__':
    iterator = jumping_range(5)
    print(next(iterator)) # 0
    print(iterator.send(2)) # 2
    print(next(iterator)) # 3
    print(iterator.send(-1)) # 2
    for x in iterator:
        print(x) # 3, 
```
> next() 等价于 send(None)

### 协程

##### 一个简单的爬虫

```

import time

def crawl_page(url):
    print('crawling {}'.format(url))
    sleep_time = int(url.split('_')[-1])
    time.sleep(sleep_time)
    print('OK {}'.format(url))

def main(urls):
    for url in urls:
        crawl_page(url)

%time main(['url_1', 'url_2', 'url_3', 'url_4'])

########## 输出 ##########

crawling url_1
OK url_1
crawling url_2
OK url_2
crawling url_3
OK url_3
crawling url_4
OK url_4
Wall time: 10 s
```

##### 用协程实现

```

import asyncio

async def crawl_page(url):
    print('crawling {}'.format(url))
    sleep_time = int(url.split('_')[-1])
    await asyncio.sleep(sleep_time)
    print('OK {}'.format(url))

async def main(urls):
    for url in urls:
        await crawl_page(url)

%time asyncio.run(main(['url_1', 'url_2', 'url_3', 'url_4']))

########## 输出 ##########

crawling url_1
OK url_1
crawling url_2
OK url_2
crawling url_3
OK url_3
crawling url_4
OK url_4
Wall time: 10 s
```

##### 协程中加入 task（任务）

```

import asyncio

async def crawl_page(url):
    print('crawling {}'.format(url))
    sleep_time = int(url.split('_')[-1])
    await asyncio.sleep(sleep_time)
    print('OK {}'.format(url))

async def main(urls):
    tasks = [asyncio.create_task(crawl_page(url)) for url in urls]
    for task in tasks:
        await task

%time asyncio.run(main(['url_1', 'url_2', 'url_3', 'url_4']))

########## 输出 ##########

crawling url_1
crawling url_2
crawling url_3
crawling url_4
OK url_1
OK url_2
OK url_3
OK url_4
Wall time: 3.99 s
```
##### 执行 tasks 的另一种方法

```

import asyncio

async def crawl_page(url):
    print('crawling {}'.format(url))
    sleep_time = int(url.split('_')[-1])
    await asyncio.sleep(sleep_time)
    print('OK {}'.format(url))

async def main(urls):
    tasks = [asyncio.create_task(crawl_page(url)) for url in urls]
    await asyncio.gather(*tasks)

%time asyncio.run(main(['url_1', 'url_2', 'url_3', 'url_4']))

########## 输出 ##########

crawling url_1
crawling url_2
crawling url_3
crawling url_4
OK url_1
OK url_2
OK url_3
OK url_4
Wall time: 4.01 s
```

##### Asyncio 用法

```

import asyncio
import aiohttp
import time

async def download_one(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print('Read {} from {}'.format(resp.content_length, url))

async def download_all(sites):
    tasks = [asyncio.create_task(download_one(site)) for site in sites]
    await asyncio.gather(*tasks)

def main():
    sites = [
        'https://en.wikipedia.org/wiki/Portal:Arts',
        'https://en.wikipedia.org/wiki/Portal:History',
        'https://en.wikipedia.org/wiki/Portal:Society',
        'https://en.wikipedia.org/wiki/Portal:Biography',
        'https://en.wikipedia.org/wiki/Portal:Mathematics',
        'https://en.wikipedia.org/wiki/Portal:Technology',
        'https://en.wikipedia.org/wiki/Portal:Geography',
        'https://en.wikipedia.org/wiki/Portal:Science',
        'https://en.wikipedia.org/wiki/Computer_science',
        'https://en.wikipedia.org/wiki/Python_(programming_language)',
        'https://en.wikipedia.org/wiki/Java_(programming_language)',
        'https://en.wikipedia.org/wiki/PHP',
        'https://en.wikipedia.org/wiki/Node.js',
        'https://en.wikipedia.org/wiki/The_C_Programming_Language',
        'https://en.wikipedia.org/wiki/Go_(programming_language)'
    ]
    start_time = time.perf_counter()
    asyncio.run(download_all(sites))
    end_time = time.perf_counter()
    print('Download {} sites in {} seconds'.format(len(sites), end_time - start_time))
    
if __name__ == '__main__':
    main()

## 输出
Read 63153 from https://en.wikipedia.org/wiki/Java_(programming_language)
Read 31461 from https://en.wikipedia.org/wiki/Portal:Society
Read 23965 from https://en.wikipedia.org/wiki/Portal:Biography
Read 36312 from https://en.wikipedia.org/wiki/Portal:History
Read 25203 from https://en.wikipedia.org/wiki/Portal:Arts
Read 15160 from https://en.wikipedia.org/wiki/The_C_Programming_Language
Read 28749 from https://en.wikipedia.org/wiki/Portal:Mathematics
Read 29587 from https://en.wikipedia.org/wiki/Portal:Technology
Read 79318 from https://en.wikipedia.org/wiki/PHP
Read 30298 from https://en.wikipedia.org/wiki/Portal:Geography
Read 73914 from https://en.wikipedia.org/wiki/Python_(programming_language)
Read 62218 from https://en.wikipedia.org/wiki/Go_(programming_language)
Read 22318 from https://en.wikipedia.org/wiki/Portal:Science
Read 36800 from https://en.wikipedia.org/wiki/Node.js
Read 67028 from https://en.wikipedia.org/wiki/Computer_science
Download 15 sites in 0.062144195078872144 seconds
```

##### 多线程还是 Asyncio
- 如果是 I/O bound，并且 I/O 操作很慢，需要很多任务 / 线程协同实现，那么使用 Asyncio 更合适
- 如果是 I/O bound，但是 I/O 操作很快，只需要有限数量的任务 / 线程，那么使用多线程就可以了
- 如果是 CPU bound，则需要使用多进程来提高程序运行效率