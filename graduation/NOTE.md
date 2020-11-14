# 一. requests 爬虫和 scrapy 爬虫

### 使用 requests 写简单的爬虫

```python
# 导入 requests 库
import requests

# 定义 user-agent
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"

# 定义请求头，是一个字典
headers = {'user-agent': user_agent}

# 定义请求地址
url = "https://movie.douban.com/top250"

# 发起 get 请求并获取响应信息
response = requests.get(url, headers=headers)

# 获取响应的状态码
print(response.status_code)
# 获取响应的内容
print(response.text)
```

[requests 官方文档链接](https://requests.readthedocs.io/zh_CN/latest/)

### 使用 BeautifulSoup 解析爬取的网页

```python
# 导入 requests 和 bs4 库
import requests
# 如果库的名称太长，可以使用 as 重命名
from bs4 import BeautifulSoup as bs

user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'

headers = {'user-agent': user_agent}
url = 'https://movie.douban.com/top250'

response = requests.get(url, headers=headers)

# 使用 bs 解析网页的源代码，解析模式是 html
soup = bs(response.text, 'html.parser')

# 筛选出想要的内容
# 找到所有 class 属性 为 hd 的 div 标签
for div in soup.find_all('div', attrs={'class':'hd'}):
  # 找到所有 a 标签
  for a in div.find_all('a',):
    # 获取 a 标签的 href 属性值
    print(a['href'])
    # 也可以通过 get 获取 href 属性值
    print(a.get('href'))
    # 找到 a 标签下的 span 标签，并取得内容
    print(a.find('span',).text)
```

[Beautiful Soup 官方文档链接](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)

### 使用 XPath 解析网页

```python
# 引入 request 库
import requests
# 引入 lxml 库
import lxml.etree

# 电影的详情页面
url = 'https://movie.douban.com/subject/1292052/'

# 定义 headers
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
headers = {'user-agent': user_agent}

# 获取页面信息
response = requests.get(url, headers=headers)

# 使用 lxml 来处理页面
xml = lxml.etree.HTML(response.text)

# 获取电影名称
film_name = xml.xpath('//*[@id="content"]/h1/span[1]/text()')

print(f'电影名称：{film_name}')

# 获取上映日期
film_date = xml.xpath('//*[@id="info"]/span[10]/text()')
print(f'上映日期：{film_date}')

# 获取评分
film_rating = xml.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
print(f'评分：{film_rating}')


# 合并电影信息
film_info = [film_name, film_date, film_rating]
print(film_info)

# 使用 Pandas 对电影信息进行保存
import pandas as pd

film = pd.DataFrame(data=film_info)

#保存到文件，unix 系统使用 utf8，windows 系统使用 gbk
film.to_csv('./film.csv', encoding='utf8', index=False, header=False)
```

### 实现爬虫的自动翻页功能

```python
# 引入 requests 和 BeautifulSoup 库
import requests
from bs4 import BeautifulSoup as bs

# 定义一个爬取单个页面信息的函数
def get_single_page(url):

  # 设置 user-agent
  user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
  # 设置 headers
  headers = {'user-agent': user_agent}

  # 发起请求并获取请求结果
  response = requests.get(url, headers=headers)

  # 利用 BeautifulSoup 对请求网页进行处理
  bs_res = bs(response.text, 'html.parser')

  # 筛选出电影名称和电影详情链接
  films = []
  for hd in bs_res.find_all('div', attrs={'class': 'hd'}):
    a = hd.find('a')
    # print(a.get('href'))
    # print(a.find('span').text)
    films.append({'name': a.find('span').text, 'href': a.get('href')})

  return films

# 设置所有分页链接
urls = tuple(f'https://movie.douban.com/top250?start={off_set * 25}&filter=' for off_set in range(10))

# 循环遍历分页链接，获取所有 top250 的电影信息
top_250_films = []
for url in urls:
  films = get_single_page(url)
  top_250_films.extend(films)

# 导入 pandas 库，将爬取到的电影信息保存
import pandas as pd

pd_obj = pd.DataFrame(data=top_250_films)
pd_obj.to_csv('./top_250_films.csv', encoding='utf8')

print('保存完毕')


```

### Python 基础语法

[Python 简介](https://docs.python.org/zh-cn/3.7/tutorial/introduction.html)

[Python 数据结构](https://docs.python.org/zh-cn/3.7/tutorial/datastructures.html)

[Python 其他流程控制工具](https://docs.python.org/zh-cn/3.7/tutorial/controlflow.html)

[Python 中的类](https://docs.python.org/zh-cn/3.7/tutorial/classes.html)

[Python 定义函数](https://docs.python.org/zh-cn/3.7/tutorial/controlflow.html#defining-functions)

##### 在交互模式中可以使用 dir 和 help 方法查看库的信息

- import math
- 使用 dir 查看库里面的所有方法，eg. dir(math)
- 使用 help 查看具体方法的使用方法，eg. help(math)

### HTML 基本结构

### HTTP 协议

### Scrapy 框架结构解析

[Scrapy 架构官方文档介绍](https://docs.scrapy.org/en/latest/topics/architecture.html)

##### Scrapy 核心组件

![TIM截图20200820082644](https://note.youdao.com/yws/res/6209/340944BA0F444D6BB5BFD4B2C181825D)

##### Scrapy 架构示意图

![TIM截图20200820082949](https://note.youdao.com/yws/res/6213/CA87FC79E4D142DB9763EDD9A3F7A901)

##### Scrapy 架构

![TIM截图20200820083041](https://note.youdao.com/yws/res/6216/092F331702D742039DE084E88ECB328B)

### Scrapy 爬虫目录结构解析

##### 安装 scrapy

```
pip install scrapy
```

##### 创建一个 scrapy 的项目

```
scrapy startproject spiders
```

##### 创建一个 spider 并指定名称和域名

```
# 项目里面的 spiders 目录
cd spiders

# 创建一个域名为 douban.com，名称为 movies 的 spider
scrapy genspider movies douban.com
```

##### 项目的目录结构

![TIM截图20200821075109](https://note.youdao.com/yws/res/6243/3D86ED77E68F48D088F4B8CC7CFB5AA9)

### 使用 Scrapy 写爬虫

##### 编写解析网页代码

代码目录：项目名称/项目名称/spiders/爬虫名称.py

```python
# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
from douban.items import DoubanItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    # def parse(self, response):
    #     pass

    # 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象（Request）。
    # start_requests()方法读取start_urls列表中的URL并生成Request对象，发送给引擎。
    # 引擎再指挥其他组件向网站服务器发送请求，下载网页
    def start_requests(self):
        for i in range(0, 10):
            url = f'https://movie.douban.com/top250?start={i * 25}&filter='
            # url 请求访问的网址
            # callback 回调函数，引擎回将下载好的页面(Response对象)发给该方法，执行数据解析
            # 这里可以使用callback指定新的函数，不是用parse作为默认的回调参数
            yield scrapy.Request(url=url, callback=self.parse)

    # 返回页面的解析函数

    def parse(self, response):

        items = []
        # 使用 BeautifulSoup 对网页进行解析
        soup = bs(response.text, 'html.parser')

        for hd in soup.find_all('div', attrs={'class': 'hd'}):
            # 在 项目名称/项目名称/items.py 中定义，需要先引入改类
            item = DoubanItem()
            element_a = hd.find('a')
            href = element_a.get('href')
            title = element_a.find('span', attrs={'class': 'title'}).text
            # item 是一个字典类型，字典的 key 需要在 item.py 中先定义好
            item['title'] = title
            item['href'] = href

            items.append(item)
        # 返回给 pipelines
        return items

```

##### 运行爬虫

```
# 进入项目目录
cd douban

# 运行爬虫
scrapy crawl movie
```

### 通过 Scrapy 爬取下一层信息

##### 在第一层页面的解析函数中继续发送请求

```python
# 返回页面的解析函数

def parse(self, response):

    # items = []
    # 使用 BeautifulSoup 对网页进行解析
    soup = bs(response.text, 'html.parser')

    for hd in soup.find_all('div', attrs={'class': 'hd'}):
        # 在 项目名称/项目名称/items.py 中定义，需要先引入改类
        item = DoubanItem()
        element_a = hd.find('a')
        href = element_a.get('href')
        title = element_a.find('span', attrs={'class': 'title'}).text
        # item 是一个字典类型，字典的 key 需要在 item.py 中先定义好
        item['title'] = title
        item['href'] = href
        # 继续发送下一层的请求，可以通过 meta 参数传递数据
        yield scrapy.Request(url=href, meta={'item': item}, callback=self.parse_detail)

        # items.append(item)
    # 返回给 pipelines
    # return items
```

##### 定义下一层页面的解析函数

```python
# 详情页面的解析函数
def parse_detail(self, response):

    soup = bs(response.text, 'html.parser')
    intro = soup.find('div', attrs={'id': 'link-report'}).get_text().strip()
    # 获取上一个页面带回的信息
    item = response.meta['item']
    item['intro'] = intro

    # 返回给 pipelines 处理
    yield item
```

##### 编写 pipelines 保存信息

```python
class DoubanPipeline:

    # 每一个item管道组件都会调用该方法，并且必须返回一个item对象实例或raise DropItem异常
    def process_item(self, item, spider):

        title = item['title']
        href = item['href']
        intro = item['intro']

        output = f'|{title}|\t|{href}|\t|{intro}|\n\n'

        # 保存到文件
        with open('./films.txt', 'a+', encoding='utf-8') as writeable:
            writeable.write(output)

        return item
```

##### 修改 settings.py 配置 pipelines

```python
ITEM_PIPELINES = {
   'douban.pipelines.DoubanPipeline': 300,
}
```

### XPath 详解

##### [Scrapy Xpath 官方学习文档](https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-xpaths)

##### [Xpath 中文文档](https://www.w3school.com.cn/xpath/index.asp)

##### [Xpath 英文文档](https://www.w3.org/TR/2017/REC-xpath-31-20170321/#nt-bnf)

##### 使用方法

```python

# 引入 scrapy 中得出 XPath 模块
from scrapy.selector import Selector

# 解析页面内容，直接放入 response
xpath_obj = Selector(response=response)

# 查找具体内容
movies = xpath.obj.xpath('//div[@class="hd"]')
for movie in movies:
    title_xpath = moive.xpath('./a/span/text()')
    link_xpath = movie.xpath('./a/@href')

    # title_xpath 是一个由 Selector 组成的列表
    # 获取具体的内容需要使用 extract() 或 extract_first()
    # extract() 表示获取所有 Selector 的内容
    # extract_first() 表示获取第一个 Selector 的内容

    title_1 = title_xpath.extract()
    title_2 = title_xpath.extract_first()
    title_3 = title_xpath.extract_first().strip()

```

> '//div[@class="hd"]' 从上到下去寻找 class 属性为 hd 的 div

> // 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置（常用）

> / 从根节点选取（路径太长不常用）

> . 选取当前节点

> .. 选取当前节点的父节点

> 取内容用 text()，注意内容中的 br，取属性用 @

##### XPath 的调试

1. 复制 XPath 到浏览器中查找
2. print 输出匹配结果

### yield 与推导式

##### [yield 表达式官方文档](https://docs.python.org/zh-cn/3.7/reference/expressions.html#yieldexpr)

##### [yield 语句官方文档](https://docs.python.org/zh-cn/3.7/reference/simple_stmts.html#yield)

##### [Python 推导式官方文档](https://docs.python.org/zh-cn/3.7/tutorial/datastructures.html#list-comprehensions)

##### yield 的使用

yield 可以作为语句和表达式来使用

yield 和 return 的区别

```python
def chain(*iterables): for it in iterables:
yield it
>>> s = 'ABC'
>>> list(chain(s))
['A', 'B', 'C']
```

##### 推导式

一个列表推导式的例子:

```python
mylist = []
for i in range(1, 11):
    if i > 5:
    mylist.append(i**2)
print(mylist)
```

转换为列表推导式:

```python
mylist = [i**2 for i in range(1, 11) if i > 5]
```

==推导式语法:[ 表达式 for 迭代变量 in 可迭代对象 if 条件 ]==

循环嵌套

```python
mylist = [str(i)+j for i in range(1, 6) for j in 'ABCDE']
```

字典转换为列表

```python
mydict = {'key1' : 'value1', 'key2' : 'value2'}
mylist = [key + ':' + value for key, value in mydict.items()]
print(mylist)
```

字典 key 和 value 互换

```python
{value: key for key, value in mydict.items()}
```

字典推导式

```python
mydict = {i: i*i for i in (5, 6, 7)}
print(mydict)
```

集合推导式

```python
myset = {i for i in 'HarryPotter' if i not in 'er'}
print(myset)
```

==元组推导式要显式使用 tuple()，不能直接使用()==

生成器

```python
mygenerator = (i for i in range(0, 11))
print(mygenerator)
print(list(mygenerator))
```

# 二. 反爬虫机制、scrapy 中间件和分布式爬虫

### 异常捕获与处理

##### [官方文档](https://docs.python.org/zh-cn/3.7/library/exceptions.html)

##### 例子


```python
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

```python
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


```python
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

```python
with open('text.txt', mode='r', encoding='utf8') as target:
    print(target.read())
```
##### 自定义 with

```python
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


```python
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


```python
# 建立游标的时候就开启了一个事务
cursor = conn.cursor()
```


##### CRUD（查询并获取数据）

```python
# 查询
sql = 'SELECT * FROM tabe'
cursor.excute(sql)

# 单个结果
result = cursor.fetchone()
# 所有结果
result = cursor.fetchall()

```

##### 关闭 cursor

```python
cursor.close()

# 实行成功则 commit
conn.commit()
# 执行出错则 rollback
conn.rollback()
```

##### 关闭 connection

```python
conn.close()
```


##### 结束



### 反爬虫

##### 请求 header 的设置

- 随机设置 User-Agent（[User-Agent 参考文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/User-Agent)）



```python
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


```python
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


```python
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
```python
import requests

image_utl = ""

r = requests.get(image_utl)
with open("download.png", "wb") as f:
    f.write(r.content)
```
大文件下载

```python
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

```python
from PIL import Image
image = Image.open('图片')

# 显示图片
image.show()
```

###### 用 Pillow 将图片灰度化

```python
gray_image = image.convert('L')
```

###### 用 Pillow 将图片二值化

```python
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

```python
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

```python
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


```python
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

# 三. 多进程和多线程

### Scrapy 并发参数优化


```python
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

```python
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


```python
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

```python
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

```python
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


```python
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


```python
# 只是为了做循环
for _ in range(5):
```

```python
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


```python
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


```python
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

```python
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


```python
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


```python
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

```python
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

```python
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

```python
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


```python
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
```python
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

```python
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

```python
import queue
q = queue.LifoQueue()
```

##### 线程池

###### [concurrent.futures - 线程池执行器](https://docs.python.org/zh-cn/3.7/library/concurrent.futures.html#threadpoolexecutor)

###### [concurrent.futures - 进程池执行器](https://docs.python.org/zh-cn/3.7/library/concurrent.futures.html#processpoolexecutor)

# 四. 数据清洗与预处理

### pandas 简介

[pandas 中文文档](https://www.pypandas.cn/)

[Numpy 学习文档](https://numpy.org/doc/)

[matplotlib 学习文档](https://matplotlib.org/contents.html)

### pandas 基本数据类型

##### Series

从列表创建 Series

```python
import pandas as pd
import numpy as np

pd.Series(['a', 'b', 'c'])
```
通过字典创建自带索引的 Series

```python
series1 = pd.Series({'a': 11, 'b': 22, 'c': 33})
```

通过关键字创建带索引的 Series

```python
series2 = pd.Series([11, 22, 33], index = ['a', 'b', 'c'])
```

获取全部索引

```python
series1.index
```
获取全部值

```python
series2.values
```
类型

```python
type(series1.values) # <class 'numpy.ndarray'>
type(np.array(['a', 'b']))
```

转化为列表

```python
series1.values.tolist()
```
> 使用 index 会提升查询性能
> 
> 如果 index 唯一，pandas 会使用哈希表优化，查询性能为 O(1)
> 
> 如果 index 有序不唯一，pandas 会使用二分查找算法，查询性能为 O(logN)
> 
> 如果 index 完全随机，每次查询都要扫全表，查询性能为 O(N)


##### DataFrame

列表创建 dataFrame

```python
df1 = pd.DataFrame(['a', 'b', 'c', 'd'])
```

嵌套列表创建 dataFrame

```python
df2 = pd.DataFrame(
    [
        ['a', 'b'],
        ['c', 'd']
    ]
)
```

自定义列索引


```python
df2.columns = ['one', 'two']
```

自定义行索引


```python
df2.index = ['first', 'second']
```


可以在创建时直接锁定

```python
df3 = pd.DataFrame([...], colums=[], index=[])
```
查看索引

```python
df2.columns
df2.index
```

### pandas 数据导入

##### Pandas 支持大量格式的导入，使用的是 read_*() 的形式


```python
import pandas as pd

pd.read_excel(r'1.xlsx')

# sep 分隔符
# nrows 读取的行数
# encoding 编码
pd.read_csv(r'c:\file.csv', sep='', nrows=10, encoding='utf-8')

# sql 查询 sql
# conn 数据库连接
pd.read_sql(sql, conn)
```


### pandas 数据预处理

##### 缺失值处理


```python
import pandas as pd
import numpy as np

x = pd.Series([1, 2, np.nan, 3, 4, 5, 6, np.nan, 8])
```

是否存在缺失值

```python
x.hasnans
```

将缺失值填充为平均值

```python
x.fillna(value = x.mean())
```

向前填充缺失值

```python
df = pd.DataFrame({
    "A": [5, 3, None, 4],
    "B": [None, 2, 4, 3],
    "C": [4, 3, 8, 5],
    "D": [5, 4, 2, None]
})

# 查看缺失值汇总
df.isnull().sum()

# 用上一行填充
df.ffill()

# 用前一列填充
df.ffill(axis=1)
```

缺失值删除

```python
df.info()
df.dropna()
```

填充缺失值

```python
df.fillna('无')
```


##### 重复值处理


```python
df.drop_duplicates()
```

### pandas 数据调整

##### 行列调整


```python
df = pd.DataFrame({"A":[5,3,None,4], 
                 "B":[None,2,4,3], 
                 "C":[4,3,8,5], 
                 "D":[5,4,2,None]}) 
```
列的选择，多个列要用列表


```python
df[ ['A', 'C'] ]
```

某几列


```python
# :表示所有行，获得第1和第3列
df.iloc[:, [0,2]]

```

行选择

```python
# 选择第1行和第3行
df.loc[ [0, 2] ]

# 选择第1行到第3行
df.loc[ 0:2 ]

# 比较，满足 A 行小于 5，C 行小于 4
df[ (df['A'] < 5) & (df['C'] < 4) ]
```


##### 数值替换

一对一替换

```python
# C 列中的 4 替换成 40
df['C'].replace(4, 40)
```

多对一替换

```python
# 4，5,8 替换成 1000
df.replace([4, 5, 8], 1000)
```

多对多替换

```python
df.replace({4: 400, 5: 500, 8: 800})
```

##### 排序


```python
# 按照指定列降序排列
df.sort_values( by = ['A'], ascending = False )
# 多列排序
df.sort_values( by = ['A', 'C'], ascending = [True, False] )
```


##### 删除


```python
# 删除列
df.drop('A', axis=1)

# 删除行
df.drop(3, axis=0)

# 删除特定行
df[ df['A'] < 4 ]
```


##### 行列互换


```python
df.T
df.T.T
```

##### 索引重塑


```python
# 数据透视表
df.stack()
df.unstack()

# 充值索引
df.stack().reset_index()

```


### pandas 基本操作

##### [Pandas 计算功能操作文档](https://pandas.pydata.org/docs/user_guide/computation.html#method-summary)

##### 算数运算

```python
df['A'] + df['C']
```

##### 比较运算

```python
df['A'] < df['C']
```

##### 非空值计数

```python
df.count()
```

##### 非空值列求和

```python
df.sum()
df['A'].sum()
```

##### 求平均值

```python
df.mean()
```

##### 求最大值

```python
df.max()
```

##### 求最小值

```python
df.min()
```

##### 求中位数

```python
df.median()
```

##### 求众数

```python
df.mode()
```

##### 求方差

```python
df.var()
```

##### 求标准差

```python
df.std()
```

### pandas 分组聚合

#####  分组

```python
import pandas as pd
import numpy as np

groups = ['x', 'y', 'z']

df = pd.DataFrame({
    'group': [groups[i] for i in np.random.randint(0, len(groups), 10)],
    "salary":np.random.randint(5,50,10),
    "age":np.random.randint(15,50,10)
})

# 分组
df.groupby('group')
```

#####  聚合计算

```python
# 分组后求平均值
df.groupby('group').agg('mean')

# 分组后求 salary 的平均值，和 age 的方差
df.groupby('group').agg( {'salary': 'mean', 'age': 'var'} )

# 如果 agg 中只有一个函数，则可以直接计算
df.groupby('group').mean()

# 计算结果转换为 python 的字典
df.groupby('group').mean().to_dict()

# 使用 transform 代替 agg
df.groupby('group').transform('mean')

# 透视表
pd.pivot_table(df, values='salary', columns='group', index='age', aggfunc='count', margins=True).reset_index()

```

### pandas 多表拼接

##### [merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)

```python
# left 左数据
# right 有数据
# how 链接方式 inner left right outer
# on 如果有多个相同字段就通过 on 指定
merge(left, right, how: str="inner", on=None, left_on=None, right_on=None, left_index: bool=False, right_index: bool=False, sort: bool=False, suffixes=("_x", "_y"), copy: bool=True, indicator: bool=False, validate=None) 
```

##### [concat](https://pandas.pydata.org/docs/reference/api/pandas.concat.html)

### pandas 输出和绘图

##### [plot 学习文档](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html)

##### [seaborn 学习文档](http://seaborn.pydata.org/tutorial.html)

##### 导出为 .xlsx 文件


```python
# excel_writer 文件名称
# sheet_name Sheet 名称
# index 是否去掉索引
# columns 要导出的列
# encoding 设置编码
# na_rep 缺失值处理
# inf_rep 无穷值处理

df.to_excel( excel_writer = f'file.xlsx', sheet_name = 'sheet1', index = False, columns = ['col1', 'col2'], encoding='utf-8', na_rep=0, inf_rep=0 )
```
##### 导出为 .csv 文件

```python
df.to_csv()
```
##### 导出为 .pkl 文件（性能好）

```python
df.to_pickle('xx.pkl')
```
> agg 中尽量使用内置函数
> 
> agg(sum) 快
> 
> agg( lambda x: x.sum() ) 慢

##### 导出为 plt 和 seaborn 图像


```python
import matplotlib.pyplot as plt

# df.index 为横坐标，df['A'] 为纵坐标
plt.plot(df.index, df['A'])

# color 颜色
# linestyle 线条颜色
# linewidth 线条宽度
# marker 点标记
plt.plot(df.index, df['A'], color='#ffaa00', linestyle='--', linewidth=3, marker='D')

# 显示
plt.show()
```

```python
import seaborn as sns

# 绘制散点图
plt.scatter(df.index, df['A'])
plt.show()

# 美化 plt
sns.set_style('darkgrid')
plt.scatter(df.index, df['A'])
plt.show()
```


### jieba 分词与提取关键词

##### [jieba 学习文档](https://github.com/fxsjy/jieba/blob/master/README.md)

##### 分词

精确模式

```python
jieba.cut(string, cut_all=False)
```

全模式

```python
jieba.cut(string, cut_all=True)
```

搜索引擎模式

```python
jieba.cur_for_search()
```

自定义用户词典

```python
jieba.load_userdict(r'user_dict.txt')
```

--user_dict.txt
```python
# 词的内容 权重 词性
Python进阶训练营 3 nt
```
动态添加词典

```python
jieba.add_word('极客大学')
```
动态删除词典

```python
jieba.del_word('自定义词')
```
关闭自动计算词频

```python
jieba.cut(string, HMM=False)
```
调整分词，合并

```python
jieba.suggest_freq('中出', True)
# 结合 HMM= False
jieba.cut(string, HMM=False)
```

调整分词，分开

```python
jieba.suggest_freq(('中','将'), True)
# 结合 HMM= False
jieba.cut(string, HMM=False)
```


##### 关键字提取

```python
# 基于TF-IDF算法进行关键词抽取
tfidf = jieba.analyse.extract_tags(text,
topK=5,                   # 权重最大的topK个关键词
withWeight=True)         # 返回每个关键字的权重值
# 基于TextRank算法进行关键词抽取
textrank = jieba.analyse.textrank(text,
topK=5,                   # 权重最大的topK个关键词
withWeight=False)         # 返回每个关键字的权重值
```

> 通过 jieba.analyse.set_stop_words('jieba/stop_words.txt') 方法添加需要排除的词


### SnowNLP 情感倾向分析

##### [snowNLP 参考学习地址](https://github.com/isnowfy/snownlp/blob/master/README.md)

中文分词

```python
from snownlp import SnowNLP

text = ''

s = SnowNLP(text)
s.words
```

词性标注（隐马尔可夫模型）

```python
s.tags
```

情感分析（朴素贝叶斯分类器）

```python
s.sentiments
```

拼音（Trie树）

```python
s.pinyin
```

繁体转简体

```python
s.han
```

提取关键字

```python
s.keywords(limit=5)
```

信息衡量

```python
# 词频越大越重要
s.tf

# idf 越大，说明词条越重要
s.idf
```

训练

```python
from snownlp import seg

seg.train('data.txt')
seg.save('seg.marshal')
```

# 五. Django 开发入门

### MTV 框架模式

#### 模型（Model）

1. 创建模型
2. 执行 CRUD

#### 模板（Template）

1. \*\*\*\*.html

#### 视图（Views）

1. 接收请求
2. 调用 models
3. 调用 Templates
4. 将数据填充到模板上再响应

### Django 的特点

#### 采用了 MTV 的框架

#### 强调快速开发和代码复用 DRY（Do Not Repeat Yourself）

#### 组件丰富

1. ORM（对象关系映射）映射类来构建数据模型
2. URL 支持正则表达式
3. 模板可继承
4. 内置用户认证，提供用户认证和权限功能
5. admin 管理系统
6. 内置表单模型、Cache 缓存系统、国际化系统等

### Django 版本安装

Django 最新 3.0 版本，目前比较多的是 2.2.13（LTS）

```
$ pip install --upgrade django==2.2.13

>>> import django
>>> django.__version__
```

### 创建 Django 项目

```
django-admin startproject MyDjango
```

> MyDjango/manage.py 命令行工具

> MyDjango/MyDjango/settings.py 项目的配置文件

### 创建 Django 应用程序

```
# 查看该工具的具体功能
python manage.py help
```

```
python manage.py startapp index
```

### 启动和停止 Django 应用程序

```
python manage.py runserver
```

> 默认是 127.0.0.1:8000

```
python manage.py runserver 0.0.0.0:80
```

退出

Control + C

### 设置 Django 的配置文件

#### 添加 App

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #### 注册自己的App
    'index',
]
```

#### 配置数据库

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
```

### 增加项目 urls

##### 1. MyDjango/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
]
```

##### 2. index/urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index)
]
```

##### 3. index/views.py

```python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello Django!")
```

### 模块和包

```python
1. 模块：.py 结尾的 Python 程序
2. 包：存放多个模块的目录
3. __init__.py 运行的初始化文件，可以是空文件
```

### URL 变量

#### 变量类型

- str
- int
- slug
- uuid
- path

```python
path('<int:year>', views.myyear)
```

#### 正则表达式

```python
from django.urls import re_path

re_path('(?P<year>[0-9]{4}).html', views.myyear, name='urlyear')
```

> ?P 表示正则

> <year> 表示变量名称

> name='urlyear' 表示 url 名称，通常在 template 中使用

#### 自定义

##### 1. index/urls.py

```python
# 导入转化器注册函数
from django.urls import path, register_converter

# 注册自定义转化器
register_converter(converters.YearConverter, type_name='myyear')

# 使用自定义转化器定义 url
path('<myyear:year>', views.year)
```

##### 2. index/converters.py

```python
class IntConverter:

    # 正则表达式
    regex = '[0-9]+'

    # 从 url 转化成 python
    def to_python(self, value):
        return int(value)

    # 从 python 转化成 url
    def to_url(self, value):
        return str(value)
```

### Django 快捷函数

##### 1. render()

将给定的模板与给定的上下文字典组合在一起，并以渲染的文本返回一个 HttpResponse 对象

##### 2. redirect()

将一个 HttpResponseRedirect 返回到传递的参数的适当 URL

##### 3. get_object_or_404()

在给定的模型管理器（model manager）上调用 get()，但它会引发 Http404 而不是模型的 DoesNotExist 异常

### ORM API

#### 常见问题

##### 1. 找不到 MySQLdb

```python
django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'
```

解决方法：在 ** init **.py 文件中添加以下代码即可

```python
import pymysql
pymysql.install_as_MySQLdb()
```

##### 2. MySQL 版本问题

```python
version = Database.version_info
```

解决方法：注释相应代码

```python
# if version < (1, 3, 13):
# raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
```

##### 3. Python 版本问题

```python
AttributeError: 'str' object has no attribute 'decode'
```

解决方法：在 operations.py 中注释相应代码

```python
def last_executed_query(self, cursor, sql, params):
    query = getattr(cursor, '_executed', None)
    # if query is not None:
    #     query = query.decode(errors='replace')
    return query
```

#### 模型与数据库

- 每一个模型都是一个 Python 的类，这些类继承 django.db.models.Model
- 模型类的每个属性都相当于一个数据库的字段
- 利用这些，Django 提供了一个自动生成访问数据库的 API

```python
from django.db import models

class Person(models.Model):

    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

##### 对应的 SQL

```python
CREATE TABLE myapp_person(
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);

```

##### 生成对应表的命令

```python
python manage.py makemigrations
python manage.py migrate
```

##### 反向创建 Models

```python
python manage.py inspectdb
python manage.py inspectdb > models.py
```

反向创建的 Model 类中包含元数据

```python
# 元数据，不属于任何一个字段的数据
    class Meta:
        # 执行 makemigrarions 和 migrate 时会忽略
        managed = False
        # 对应表的名称
        db_table = 't1'
```

### 模板

- 模板变量 {{ variables }}
- 从 URL 获取模板变量 {% url 'urlyear' 2020 %}

> 其中 urlyear 是 urls.py 中定义的名称，2020 是传入的参数

- 读取静态资源内容 {% static "css/header.css" %}
- for 遍历标签 {% for type in type_list %} {% endfor %}
- if 判断标签 {% if name.type == type.type %} {% endif %}

### manage.py 做了什么

1. 解析 manage.py 的 runserver 和 IP 端口参数
2. 找到 command 目录加载 runserver.py
3. 检查 INSTALL_APP、IP 地址、端口、ORM 对象
4. 实例化 wsgiserver
5. 动态创建类并接收用户的请求

# 六. 面向对象编程

### 类属性和对象属性

##### 区别

1. 类属性字段在内存中只保存一份
2. 对象属性在每个对象中都保存一份

### 类的属性作用域

- \_name 人为约定不可修改
- \_\_name 私有属性
- \_\_name\_\_ 魔术方法

> 私有属性是可以访问到的，Python 通过改名机制隐藏了变量名称

### 类的方法描述器

##### 三种方法

> 三种方法在内存中都归属于类

- 普通方法：至少一个 self 参数，表示该方法的对象
- 类方法：至少一个 cls 参数，表示该方法的类
- 静态方法：由类调用，无参数

> 类方法可以通过实例调用，实例调用方法的逻辑是先找实例的方法，再找实例所在类中的方法

##### 类方法

###### 定义

类方法其实是构造函数，类当中有且只有一个构造函数 \_\_new\_\_()，不能够满足需求

###### 类方法的两大使用场景

- 定义到父类中，当使用子类，子类需要根据自己的变量名发生变化的时候可以引用到父类的 classmethod
- 当函数去调用类，并且返回我们的类的时候

##### 静态方法

### 特殊属性和方法

##### \_\_init()\_\_

- \_\_init\_\_() 方法所做的工作是在类的对象创建好之后进行变量的初始化
- \_\_init\_\_() 方法不需要显式返回，默认为 None，否则会在运行时抛出 TypeError

##### self

- self 表示实例对象本身
- self 不是 Python 的关键字(cls 也不是)，可以将 self 替换成任何你喜欢的名称，如 this、obj 等，实际效果和 self 是一样的(不推荐)
- 在方法声明时，需要定义 self 作为第一个参数，调用方法的时候不用传入 self

### 描述器高级应用

##### \_\_getattribute\_\_()

拦截获取属性，并对其进行扩展

##### \_\_getattr\_\_()

获取到不存在的属性的时候可以进行处理

##### 异同

- 都可以对==实例==属性进行获取拦截
- \_\_getattr\_\_() 适用于未定义的属性
- \_\_getattribute\_\_() 对所有属性的访问都会调用该方法

##### 注意事项

- 无论是属性存在或者不存在，getattribute 都会去调用，对性能会有所损耗
- 在使用 getattr 的时候 \_\_dict\_\_ 里面依然没有这个属性，hasattr 可能为 True

### 属性描述符

描述器：实现特定协议（描述符）的类

property 类需要实现 \_\_get**、\_\_set**、\_\_delete\_\_ 方法

property 的优点

1. 代码更简洁，可读性、可维护性更强
2. 更好的管理属性的访问
3. 控制属性访问权限，提高数据安全性

### 继承

##### object 和 type 的关系

- object 和 type 都属于 type 类 (class 'type')
- type 类由 type 元类自身创建的。object 类是由元类 type 创建
- object 的父类为空，没有继承任何类
- type 的父类为 object 类 (class 'object')

##### 单一继承

##### 多重继承

多重继承的顺序问题

1. subclass.mro()
2. 有向无环图（DAG）

##### 钻石继承

##### 继承机制 MRO

##### MRO 的 C3 算法

### SOLID 设计原则

- 单一责任原则
- 开放封闭原则
- 里氏替换原则
- 依赖倒置原则
- 接口分离原则

### 设计模式

##### 单例模式

\_\_init** 和 \_\_new** 的区别

- \_\_new\_\_ 是实例创建之前被调用，返回该实例对象，是静态方法
- \_\_init\_\_ 是实例对象创建完成后被调用，是实例方法
- \_\_new** 先被调用，\_\_init** 后被调用
- \_\_new** 的返回值(实例)将传递给 \_\_init** 方法的第一个参数，\_\_init\_\_ 给这个
  实例设置相关参数

创建单实例的方法

1. 装饰器的方式（没有多线程的推荐方式）
2. \_\_new\_\_ 的方式（线程安全的）
3. import 方式（最简单、最安全）

##### 工厂模式

### 元类

元类是关于类的类，是类的模板

元类是用来控制如何创建类的，正如类是创建对象的模板一样

元类的实例为类，正如类的实例为对象

创建元类的两种方法

1. class
2. type

> type( 类名, 父类的元组(可以为空), 类的成员(字典) )

```python
# 使用type元类创建类
def hi():
    print('Hi metaclass')

# type的三个参数:类名、父类的元组、类的成员
Foo = type('Foo',(),{'say_hi':hi})
foo = Foo
foo.say_hi()
# 元类type首先是一个类，所以比类工厂的方法更灵活多变，可以自由创建子类来扩展元类的能力
```

```python
def pop_value(self,dict_value):
    for key in self.keys():
        if self.__getitem__(key) == dict_value:
            self.pop(key)
            break

# 元类要求,必须继承自type
class DelValue(type):
    # 元类要求，必须实现new方法
    def __new__(cls,name,bases,attrs):
        attrs['pop_value'] = pop_value
        return type.__new__(cls,name,bases,attrs)

class DelDictValue(dict,metaclass=DelValue):
    # python2的用法，在python3不支持
    # __metaclass__ = DelValue
    pass

d = DelDictValue()
d['a']='A'
d['b']='B'
d['c']='C'
d.pop_value('C')
for k,v in d.items():
    print(k,v)
```

### mixin 模式

在程序运行过程中，重定义类的继承，即动态继承

好处

1. 可以在不修改任何源代码的情况下，对已有类进行扩展
2. 进行组件的划分

# 七. Python 高阶语法

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

```python
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

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(10, y=20)
p.x + p.y
p[0] + p[1]
x, y = p
```

- Counter 计数器

```python
from collections import Counter

mystring = ['a', 'b', 'c', 'c', 'c', 'a', 'b', 'd', 'e']
// 取得频率最高的前三个值
cnt = Counter(mystring)
cnt.most_common(3)
cnt['b']
```

- deque 双向队列

```python
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

```python
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


```python
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


```python
def line_conf(a, b):
    def line(x):
        return a*x+b
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5), line2(5))
```

```python
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

```python
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

```python
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

```python
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

```python
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

```python
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

```python
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

```python
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


```python
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

```python
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

```python

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

```python

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

```python

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

```python

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

```python

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


# 八. Django 开发进阶

### 源码学习方法
1. 查看官方文档
2. 记住一个官方文档的 demo
3. 记住注意事项

### Django 源码学习内容
#### 1. manage.py 源码
#### 2. URLconf 源码 --- 偏函数

##### partial 函数的实现

```python
def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*args, *fargs, **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc
```

##### partial 函数的 demo

```python
from functools import partial
basetwo = partial(int, base=2)
basetwo.__doc__ = 'Convert base 2 string to an int'
basetwo('10010')
# 输出 18
```

##### partial 函数的注意事项
- partial 第一个参数必须是可调用对象
- 参数传递顺序是从左到右，但不能超过原函数参数个数
- 关键字参数会覆盖 partial 中定义好的参数

#### 3. view 源码 --- HttpRequest 和 HttpResponse

##### [从请求到响应流程](https://hitesh.in/2009/django-flow/)

#### 4. ORM 源码 --- 元类
#### 5. Template 源码 --- render 方法的实现


### DjangoWeb 相关功能

#### 1. 管理页面

##### a. 初始化数据库


```
python manage.py migrate
```

##### b. 创建管理员账号

```
python manage.py createsuperuser
```

##### c. 增加模型

> app_name/admin.py


```python
from .models import ClassA, ClassB

admin.site.register(ClassA)
admin.site.register(ClassB)
```


#### 2. 表单与 Auth

##### a. 使用 Form 对象定义表单

> app_name/form.py

```python
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
```

> app_name/views.py

```python
from .from import LoginForm

login_form = LoginForm()

return render(request, 'demo.html', {form: login_form})
```
> templates/demo.html

```html
<form action="/demo" method="post">
    {% csrf_token %}
    {{ form }}
</form>
```

##### b. 表单与 auth 功能结合

> app_name/views.py

```python
from django.contrib.auth import authenticate, login

if request.method == 'POST':
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        # 读取表单的返回值
        cd = login_form.cleaned_data 
        user = authenticate(username=cd['username'], password=cd['password'])
        if user:
            # 登陆用户
            login(request, user)  
            return HttpResponse('登录成功')
        else:
            return HttpResponse('登录失败')
```



#### 3. 信号

a. 函数方式注册回调函数

> app_name/views.py

```python
from django.core.signals import request_started

def my_callback(sender, **kwargs):
    pass

request_started.connect(my_callbak)
```


b. 装饰器方式注册回调函数

> app_name/views.py

```python
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def my_callback(sender, **kwargs):
    pass
```

#### 4. 中间件

a. 编写中间件代码

> app_name/middleware.py

```python
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print("Process Request!")

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("Process View!")

    def process_exception(self, request, exception):
        print("Process Exception!")

    def process_response(self, request, response):
        print('Process Response!')
        return response

```

b. 注册中间件

> settings.py

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'index.middleware.MyMiddleware',
]
```
### 生产环境部署


```
pip3 install gunicorn

gunicorn MyDjango.wsgi
```
### Celery

> Celery 是分布式消息队列

> 使用 Celery 实现定时任务

a. 安装 redis

b. 安装 Celery

```
pip install celery
pip install redis==2.10.6
pip install celery-with-redis
pip install django-celery
```

> 考虑到 async 是关键字，需要替换 kombu 目录

c. 添加 Aapp

```python
django-admin startproject MyDjango
python manager.py startapp djcron

INSTALL_APPS = [
    'djcelery',
    'djcron'
]
```
d. 迁移生成表

```
python manager.py migrate
```
e. 配置 django 时区

> settings.py

```python
from celery.schedules import crontab
from celery.schedules import timedelta
import djcelery

djcelery.setup_loader()
BROKER_URL = 'redis://:123456@127.0.0.1:6379/'
CELERY_IMPORTS = ('djcron.tasks') # app
CELERY_TIMEZONE = 'Asia/Shanghai' # 时区
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # 定时任务调度器
```
f. 在 MyDjango 下面建立 celery.py

```python
import os
from celery import Celery, platforms
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','MyDjango.settings')
app = Celery('MyDjango')
app.config_from_object('django.conf:settings') 
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) 
platforms.C_FORCE_ROOT = True
```
g. 在 \_\_init__.py 增加

```python
# 使用绝对引入，后续使用import引入会忽略当前目录下的包
from __future__ import absolute_import
from .celery import app as celery_app
```
h. 增加任务

> djcron/tasks.py

```python
from MyDjango.celery import app

@app.task()
def task1():
    return 'test1'
    
@app.task()
def task2():
    return 'test2'
```
