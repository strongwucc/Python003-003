### 异常捕获与处理

##### [官方文档](https://docs.python.org/zh-cn/3.7/library/exceptions.html)

##### 例子


```
# 定义一个生成器
iterator = (i for i in range(0, 2))

try:
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
except StopIteration as e:
    print("没有更多的了")

```

##### 异常处理机制的原理

- 异常也是一个类
- 异常捕获过程

- - 异常类把错误消息打包到一个对象
- - 然后该对象会自动查找到调用栈
- - 直到运行系统找到明确声明如何处理这些异常的位置


- 所有异常继承自 BaseException
- Traceback 显示了出错的位置，显示的顺序和异常信息对象传播的方向是相反的

##### 异常信息与异常捕获

- try...except 支持多重异常处理
- ==如果设置了多个异常的捕获，则第一个异常捕获后，后面的异常将不会捕获==

```
def a():
    b()

def b():
    c()

def c():
    a = []
    print(a[1])
    # d 函数中的异常不会捕获
    d()

def d():
    print(1/0)

try:
    a()
except (ZeroDivisionError, IndexError) as e:
    print(e)
```


##### 自定义异常


```
# 自定义异常类，继承 Exception
class MyCustomException(Exception):
    def __init__(self, errorInfo):
        # 调用父类的 __init__ 方法
        super().__init__(self, errorInfo)
        self.errorInfo = errorInfo
    # __str__ 使类能以字符串的形式输出
    def __str__(self):
        return self.errorInfo


age = input()

try:
    if not age.isdigit():
        raise MyCustomException('出错啦')
    else:
        print(type(age))
        print('成功执行')
except MyCustomException as e:
    print(e)
finally:
    del age
    print('永远会执行')
```


##### 异常结果的美化


```
pip3 install pretty_errors

import pretty_errors
```


##### with 上下文协议的使用

```
with open('text.txt', mode='r', encoding='utf8') as target:
    print(target.read())
```
##### 自定义 with

```
class MyOpen():

    # 开始的时候执行
    def __enter__(self):
        print('open')

    # 结束的时候执行，参数固定
    def __exit__(self, type, value, trace):
        print('close')

    # 将类伪装成函数调用
    def __call__(self):
        pass

with MyOpen() as target:
    print('binggo')
```

### PyMySQL 的使用

##### [PyMySQL 官方文档](https://pypi.org/project/PyMySQL/)

安装 pymysql

```
pip3 install pymysql
```

##### 开始

##### 创建 connection


```
# 导入 pymysql
impory pymysql

# 创建连接
conn = pymysql.connect({
    host = '',      # ip
    prot = 3306,    # 端口 
    user = '',      # 用户名
    password = '',  # 密码
    db = ''         # 数据库名称
})
```
==port should be of type int==

##### 获取 cursor


```
# 建立游标的时候就开启了一个事务
cursor = conn.cursor()
```


##### CRUD（查询并获取数据）

```
# 查询
sql = 'SELECT * FROM tabe'
cursor.excute(sql)

# 单个结果
result = cursor.fetchone()
# 所有结果
result = cursor.fetchall()

```

##### 关闭 cursor

```
cursor.close()

# 实行成功则 commit
conn.commit()
# 执行出错则 rollback
conn.rollback()
```

##### 关闭 connection

```
conn.close()
```


##### 结束



### 反爬虫

##### 请求 header 的设置

- 随机设置 User-Agent（[User-Agent 参考文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/User-Agent)）



```
# 安装 fake-useragent 库
pip3 install fake-useragent

# 引入 UserAgent
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

# 模拟不同的浏览器
print(f'Chrome 浏览器：{ua.chrome}')
print(f'Safari 浏览器：{ua.safari}')
print(f'IE 浏览器：{ua.ie}')

# 随机返回头部信息
print(ua.random)
```

- 设置 referer 和 host (有的网站会验证)

##### cookies 验证


```
import requests

# 会话对象：在同一个 Session 实例发出的所有请求之间保持 cookie， 
# 期间使用 urllib3 的 connection pooling 功能。
# 向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。
s = requests.Session()

# 随机设置 User-Agent
ua = UserAgent(verify_ssl=False)
user_agent = ua.random

# 设置 headers
headers = {
    'User-Agent': user_agent,
    'Referer': 'https://accounts.douban.com/passport/login?source=movie'
}

# 请求地址
post_url = 'https://accounts.douban.com/j/mobile/login/basic'

# 请求信息
post_data = {
    'ck': '',
    'name': 'boen0101@163.com',
    'password': 'shanhuan30',
    'remember': 'false',
    'ticket': ''
}

# 发起登录请求
response = r.post(post_url, data=post_data, headers=headers)

resp_data = response.json()
print(resp_data)

# 再次请求用户主页验证是否能够成功获取
try:
    if resp_data['status'] == "success":
        uid = resp_data['payload']['account_info']['uid']
        resp_user = r.get(f'https://www.douban.com/people/{uid}/', headers=headers)
        print(resp_user.text)
    else:
        print(f'登录失败了：{resp_data["description"]}')
except Exception as e:
    print(f'出错啦：{e}')
```
==在同一个 Session 实例发出的所有请求之间保持 cookie， 期间使用 urllib3 的 connection pooling 功能。向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。==

##### 使用 WebDriver


```
# 导入 webdriver 库
from selenium import webdriver

# 将所有模拟浏览器的操作放在 try except 中
try:
    # 模拟一个浏览器
    browser = webdriver.Chrome()
    
    # 要能够让webdriver和Chrome建立连接，需要安装 chrome driver，版本和浏览器版本保持一致
    # http://chromedriver.storage.googleapis.com/index.html
    
    # 打开浏览器
    browser.get('https://www.douban.com')
    
    # 切换 frame
    browser.switch_to.frame(browser.find_elements_by_tag_name('iframe')[0])
    
    # 通过 xpath 查找，并模拟点击
    btm1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    btm1.click()
    
    # 通过 xpath 查找到用户名输入框，并输入用户名
    browser.find_element_by_xpath('//*[@id="username"]').send_keys('boen0101@163.com')
    
    # 通过 xpath 查找到密码输入框，并输入密码
    browser.find_element_by_id('password').send_keys('boen0101@163.com')
    
    # 通过 xpath 找到登录按钮并模拟点击
    browser.find_element_by_xpath('//a[contains(@class, "btn-account")]').click()
    
    # 获取登录后的 cookies
    cookies = browser.get_cookies()
    
except Exception as e
    print(e)
    
finally:
    # 关闭浏览器
    browser.close()
```
[Selenium with Python中文文档](https://selenium-python-zh.readthedocs.io/en/latest/index.html)

##### 模块化下载

小文件下载
```
import requests

image_utl = ""

r = requests.get(image_utl)
with open("download.png", "wb") as f:
    f.write(r.content)
```
大文件下载

```
import requests

file_url = ""

r = requests.get(file_url, stream=True)
with open("download.file", "wb") as f:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            f.wirte(chunk)
```


##### 验证码的识别

###### 先安装 tesseract

[GitHub](https://github.com/tesseract-ocr/tesseract)

macOS

```
# 先安装 libpng，jpeg，libtiff，leptonica
brew install leptonica

# 再安装 tesseract
brew install resseract

```
windows

1. [下载地址](https://github.com/UB-Mannheim/tesseract/wiki)
1. 直接执行下载好的 exe 文件，下一步、下一步默认安装即可
1. 增加安装目录到系统标量 Path
1. 增加系统变量 TESSDATA_PREFIX，变量值为 tessdata 文件夹的路径
1. 进入 cmd 验证

```
tesseract --version
```

###### 安装与 python 对接的库

```
pip3 install Pillow
pip3 install pytesseract
```

###### 下载验证码图片

###### 用 Pillow 打开图片

```
from PIL import Image
image = Image.open('图片')

# 显示图片
image.show()
```

###### 用 Pillow 将图片灰度化

```
gray_image = image.convert('L')
```

###### 用 Pillow 将图片二值化

```
throhold = 100
table = []

for i in range(255):
    if i > throhold:
        table.append(1)
    else:
        table.append(0)

gray_image.point(table, '1')
```

###### 用 pytesseract 将图片转化成字符串

```
pytesseract.image_to_string(grap_image, lang='chi_sim+eng')
```
### scrapy 中间件和代理 IP

##### scrapy 中间件

- ==Downloader Middlewares（下载中间件）==
- - 设置 headers cookies
- - ==修改 ip==


- Spider Middlewares（Spider 中间件）


##### 设置系统代理 IP

1. 设置代理 IP 的环境变量


```
# macOS
export http_proxy = 'http://52.179.231.206:80'
```


2. setting 增加中间件配置

```
DOWNLOADER_MIDDLEWARES = {
    # 自定义下载中间件
    'proxyspiders.middlewares.ProxyspidersDownloaderMiddleware': 543,
    # 系统的代理中间件 
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
    # 系统的 UserAgent 中间件
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
}
```

##### 自定义下载中间件

###### process_request(request, spider)

> request 对象经过下载中间件时会被调用，优先级高先调用

###### process_response(request, response, spider)

> response 对象经过下载中间件时会被调用，优先级高后调用

###### process_exception(request, exception, spider)

> 当 process_response() 和 process_request() 抛出异常时会被调用

###### from_crawler(cls, crawler)

> 使用 crawler 来创建中间件对象，并（必须）返回一个中间件对象

### 分布式爬虫

>Scrapy 原生不支持分布式，多机之间需要 Redis 实现队列和管道的共享
> scrapy-redis 很好地实现了 Scrapy 和 Redis 的集成

##### 使用 scrapy-redis 之后 Scrapy 的主要变化
1. 使用了 RedisSpider 类替代了 Spider 类
2. Scheduler 的 queue 由 Redis 实现
3. item pipeline 由 Redis 实现

##### 使用方法

[scrapy-redis 文档](https://github.com/rmax/scrapy-redis)

安装 scrapy-redis 库

```
pip3 install scrapy-redis
```
设置 settings.py


```
# Redis 信息
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# Scheduler 的 QUEUE
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

# 去重
DUPEILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

# Requests 的默认优先队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# 将 Requests 队列持久化到 Redis，可支持暂停或重启爬虫
SCHEDULER_PERSIST = True

# 将爬取到的 items 保存到 Redis
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}
```
