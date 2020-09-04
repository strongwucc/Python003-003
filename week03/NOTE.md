### Scrapy 并发参数优化


```
# 最大的请求数量
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# 下载延迟时间
# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
# 对单个网站进行并发请求的最大值
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# 对单个IP进行并发请求的最大值。如果非0，则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定， 使用该设定。 也就是说，并发限制将针对IP，而不是网站
CONCURRENT_REQUESTS_PER_IP = 16

```

###### Scrapy 使用的是 Twisted 模型
> Twisted是异步编程模型，任务之间互相独立， 用于大量I/O密集操作


###### [Twisted 学习参考文档](https://pypi.org/project/Twisted/)

###### [asyncio — 异步 I/O 学习文档](https://docs.python.org/zh-cn/3.7/library/asyncio.html)

### 多进程
[基于进程的并行学习文档](https://docs.python.org/zh-cn/3.7/library/multiprocessing.html)
##### 产生新进程的方式

###### 1. os.fork()
> 基于 macOS 和 Linux 系统，Windows 不支持

###### 2. multiprocessing.Process()
> 常用，推荐

##### multiprocessing 的基本使用

[multiprocessing – 基于进程的并行学习文档](https://docs.python.org/zh-cn/3.7/library/multiprocessing.html)

```
from multiprocessing import Process

def f(name):
    print(f'hello {name}')

if __name__ == '__main__':
    p = Process(target=f, args=('john',))
    p.start()
    p.join()
```

> 参数说明
> 
> multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})
> 
> - group：分组，实际上很少使用
> - target：表示调用对象，你可以传入方法的名字
> - name：别名，相当于给这个进程取一个名字
> - args：表示被调用对象的位置参数==元组==，比如 target 是函数 a，他有两个参数 m，n，那么 args 就传入 (m, n) 即可
> - kwargs：表示调用对象的字典

> 注意事项
> 
> join([timeout])
> 
> 如果可选参数 timeout 是 None （默认值），则该方法将阻塞，直到调用 join() 方法的进程终止。如果 timeout 是一个正数，它最多会阻塞 timeout 秒
> 
> 请注意，如果进程终止或方法超时，则该方法返回 None，检查进程的 exitcode 以确定它是否终止
> 
> 一个进程可以合并多次，进程无法并入自身，因为这会导致死锁，尝试在启动进程之前合并进程是错误的


##### 多进程程序的调试技巧

1. 注释 #
2. 打印 print
3. 内置函数


```
import os
import multiprocessing

# 父进程
os.getppid()

# 当前进程
os.getpid()

# 当前进程下的活动的子进程
for p in multiprocessing.active_children():
    print(f'子进程名称：{p.name}，子进程 id：{p.id}')
    
# 获取 CPU 核心数量
multiprocessing.cpu_count()
```

##### 多进程之间的通信

> 问题：
> 
> 全局变量在多个进程中不能共享，在子进程中修改全局变量对父进程中的全局变量没有影响
> 父进程在创建子进程时对全局变量做了备份，父进程中的全局变量与子进程的全局变量完全是不同的两个变量

1. 队列
> 先进先出

```
# 引入 queue
from multiprocessing import Queue

# 实例化一个队列，maxsize 可选参数定义队列的大小
q = Queue([maxsize])

# 放入队列
q.put()

# 从队列取出
q.get()
```


2. 管道

```
# 引入 pipe
from multiprocessing import Pipe

# Pipe() 函数返回一个由管道连接的连接对象，默认情况下是双工（双向）
# 返回的两个连接对象 Pipe() 表示管道的两端
parent_conn, child_conn = Pipe()

# 每个连接对象都有 send() 和 recv() 方法（相互之间的）
child_conn.send([1,2,3])
parent_conn.recv()

# 请注意，如果两个进程（或线程）同时尝试读取或写入管道的 同一 端，
# 则管道中的数据可能会损坏。当然，同时使用管道的不同端的进程不存在损坏的风险。
```

3. 共享内存


```
# 共享内存 shared memory 可以使用 Value 或 Array 将数据存储在共享内存映射中
from multiprocessing import Value, Array

# d 表示双精度浮点数， i 表示有符号整数
num = Value('d', 0.0)
arr = Array('i', range(10))

# 修改
num.value = 3.1415927
```


##### 多进程的资源抢占

1. 加锁机制


```
# 只是为了做循环
for _ in range(5):
```

```
# 在使用多进程中，你会发现打印的结果发生错行。
# 这是因为 python 的 print 函数是线程不安全的，从而导致错行。
# 解决方法也很简单，给 print 加一把锁就好了
from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()
```

##### 进程池

###### 利用 random.choice 来 sleep 不同的时间

###### 进程池的使用


```
# 引入 Pool
from multiprocessing.pool import Pool

# 创建多个进程，表示可以执行的进程的数量，默认大小是 CPU 的核心数
p = Pool(4)

# 创建进程，放入进程池统一管理
# run 函数的对象，args 函数的参数
p.apply_async(run, args=(param,))

# 如果使用的是进程池，在调用 join() 之前必须先要 close()，并且在 close() 之后不能再继续往进程池添加新的进程
p.close()
p.join()

# 一旦运行到此步，不管任务是否完成，立即终止
p.terminate()
```
==如果使用的是进程池，在调用 join() 之前必须先要 close()，并且在 close() 之后不能再继续往进程池添加新的进程==

###### 使用 with 和 map 对进程池进行扩展


```
# 使用关键字参数增加可读性
with Pool(processes=4) as pool:
    # 执行一个子进程
    result = pool.apply_async(f, (param,))
    # 显示执行结果，并设置超时时间
    print(result.get(timeout=1))
    
    result = pool.apply_async(time.sleep, (10,))
    # 超时则抛出 multiprocessing.TimeoutError
    print(result.get(timeout=1))
```

```
with Pool(processes=4) as pool:
    print(pool.map(f, range(10)))
    # 输出列表，f 只接受一个参数
    
    it = pool.imap(f, range(10))
    # 输出迭代器，f 只接受一个参数
    next(it)
    it.next(timeout=1)
```


##### [os 模块学习文档](https://docs.python.org/zh-cn/3.7/tutorial/stdlib.html#operating-system-interface)
##### [multiprocessing – 基于进程的并行学习文档](https://docs.python.org/zh-cn/3.7/library/multiprocessing.html)

### 多线程

[基于线程的并行学习文档](https://docs.python.org/zh-cn/3.7/library/threading.html)

[底层多线程 API](https://docs.python.org/zh-cn/3.7/library/_thread.html)

##### 多线程的使用

###### 函数

```
# 导入 threading 库
import threading

# 这个函数名可随便定义
def run(n):
    print("current task：", n)

if __name__ == "__main__":
    t1 = threading.Thread(target=run, args=("thread 1",))
    t2 = threading.Thread(target=run, args=("thread 2",))
    t1.start()
    t2.start()

    
# 调用方
# 阻塞  得到调用结果之前，线程会被挂起
# 非阻塞 不能立即得到结果，不会阻塞线程

# 被调用方 
# 同步 得到结果之前，调用不会返回
# 异步 请求发出后，调用立即返回，没有返回结果，通过回调函数得到实际结果
```

###### 类


```
import threading

class MyThread(threading.Thread):
    def __init__(self, n):
        super().__init__()
        self.n = n

    # 重构run函数必须要写
    def run(self):
        print("current task：", self.n)

if __name__ == "__main__":
    t1 = MyThread("thread 1")
    t2 = MyThread("thread 2")

    t1.start()
    t2.start()
    # 将 t1 和 t2 加入到主线程中，子线程结束了主线程才结束
    t1.join()
    t2.join()
```

==重构 run 函数必须要写==

##### 线程锁

[锁对象学习文档](https://docs.python.org/zh-cn/3.7/library/threading.html#lock-objects)

[递归锁对象](https://docs.python.org/zh-cn/3.7/library/threading.html#rlock-objects)

###### 普通锁的使用


```
# 引入 threading
import threading

# 定义一个锁
lock = threading.Lock() # 不可嵌套，会导致死锁
lock = threading.RLock() # 可以嵌套

# 获取锁
lock = acquire()

# 释放锁
lock = release()
```

###### 条件锁

```
# 引入 threading
import threading

# 定义一个锁
lock = threading.Condition()

# 获取锁
lock = acquire()
lock.wait_for(condition)  # 这个方法接受一个函数的返回值

# 释放锁
lock = release()
```
==条件锁的原理跟设计模式中的生产者／消费者（Producer/Consumer）模式类似==

###### 信号量

```
# 引入 threading
import threading

# 定义一个信号量
semaphore = threading.BoundedSemaphore(5)  # 最多允许5个线程同时运行

# 获取锁
semaphore = acquire()

# 释放锁
semaphore = release()
```

###### 事件锁

```
# 引入 threading
import threading

# 定义一个事件
event = threading.Event()

# 检测当前event是什么状态，如果是红灯，则阻塞，
# 如果是绿灯则继续往下执行。默认是红灯。
event = wait()

# 主动将状态设置为红灯
event.clear()

# 主动将状态设置为绿灯
event.set()
```

==通过 redis 实现分布式锁==

###### 定时器


```
import threading
import time

def run(i):

    print(f'{i}线程开始')
    time.sleep(1)
    print(f'{i}线程结束')

for i in range(10):
    thread = threading.Timer(interval=1, function=run, args=(i,))
    thread.start()
```
> interval 表示几秒后执行
> 
> function 执行的函数
> 
> args 执行函数的参数


##### 队列

[queue 学习文档](https://docs.python.org/zh-cn/3.7/library/queue.html)

###### 普通队列
```
import queue
q = queue.Queue(5)  # 设置最大上限
q.put(111)          # 存队列
q.put(222)
q.put(333)
 
print(q.get())      # 取队列
print(q.get())
q.task_done()       # 每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，
                    # 以提示q.join()是否停止阻塞，让线程继续执行或者退出
print(q.qsize())    # 队列中元素的个数， 队列的大小
print(q.empty())    # 队列是否为空
print(q.full())     # 队列是否满了
```
###### 优先级队列

```
import queue
q = queue.PriorityQueue()
# 每个元素都是元组
# 数字越小优先级越高
# 同优先级先进先出
q.put((1,"work"))
q.put((-1,"life"))
q.put((1,"drink"))
q.put((-2,"sleep"))
print(q.get())
print(q.get())
print(q.get())
print(q.get())
```
###### 后进先出队列

```
import queue
q = queue.LifoQueue()
```

##### 线程池

###### [concurrent.futures - 线程池执行器](https://docs.python.org/zh-cn/3.7/library/concurrent.futures.html#threadpoolexecutor)

###### [concurrent.futures - 进程池执行器](https://docs.python.org/zh-cn/3.7/library/concurrent.futures.html#processpoolexecutor)