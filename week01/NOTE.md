### 使用 requests 写简单的爬虫

```
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

```
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

```
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

```
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

```
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

```
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

```
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

```
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

```
ITEM_PIPELINES = {
   'douban.pipelines.DoubanPipeline': 300,
}
```

### XPath 详解

##### [Scrapy Xpath 官方学习文档](https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-xpaths)

##### [Xpath 中文文档](https://www.w3school.com.cn/xpath/index.asp)

##### [Xpath 英文文档](https://www.w3.org/TR/2017/REC-xpath-31-20170321/#nt-bnf)

##### 使用方法

```

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

```
def chain(*iterables): for it in iterables:
yield it
>>> s = 'ABC'
>>> list(chain(s))
['A', 'B', 'C']
```

##### 推导式

一个列表推导式的例子:

```
mylist = []
for i in range(1, 11):
    if i > 5:
    mylist.append(i**2)
print(mylist)
```

转换为列表推导式:

```
mylist = [i**2 for i in range(1, 11) if i > 5]
```

==推导式语法:[ 表达式 for 迭代变量 in 可迭代对象 if 条件 ]==

循环嵌套

```
mylist = [str(i)+j for i in range(1, 6) for j in 'ABCDE']
```

字典转换为列表

```
mydict = {'key1' : 'value1', 'key2' : 'value2'}
mylist = [key + ':' + value for key, value in mydict.items()]
print(mylist)
```

字典 key 和 value 互换

```
{value: key for key, value in mydict.items()}
```

字典推导式

```
mydict = {i: i*i for i in (5, 6, 7)}
print(mydict)
```

集合推导式

```
myset = {i for i in 'HarryPotter' if i not in 'er'}
print(myset)
```

==元组推导式要显式使用 tuple()，不能直接使用()==

生成器

```
mygenerator = (i for i in range(0, 11))
print(mygenerator)
print(list(mygenerator))
```
