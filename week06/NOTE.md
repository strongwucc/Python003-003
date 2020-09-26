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

```
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

```
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

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
]
```

##### 2. index/urls.py

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index)
]
```

##### 3. index/views.py

```
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello Django!")
```

### 模块和包

```
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

```
path('<int:year>', views.myyear)
```

#### 正则表达式

```
from django.urls import re_path

re_path('(?P<year>[0-9]{4}).html', views.myyear, name='urlyear')
```

> ?P 表示正则

> <year> 表示变量名称

> name='urlyear' 表示 url 名称，通常在 template 中使用

#### 自定义

##### 1. index/urls.py

```
# 导入转化器注册函数
from django.urls import path, register_converter

# 注册自定义转化器
register_converter(converters.YearConverter, type_name='myyear')

# 使用自定义转化器定义 url
path('<myyear:year>', views.year)
```

##### 2. index/converters.py

```
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

```
django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'
```

解决方法：在 ** init **.py 文件中添加以下代码即可

```
import pymysql
pymysql.install_as_MySQLdb()
```

##### 2. MySQL 版本问题

```
version = Database.version_info
```

解决方法：注释相应代码

```
# if version < (1, 3, 13):
# raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
```

##### 3. Python 版本问题

```
AttributeError: 'str' object has no attribute 'decode'
```

解决方法：在 operations.py 中注释相应代码

```
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

```
from django.db import models

class Person(models.Model):

    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

##### 对应的 SQL

```
CREATE TABLE myapp_person(
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);

```

##### 生成对应表的命令

```
python manage.py makemigrations
python manage.py migrate
```

##### 反向创建 Models

```
python manage.py inspectdb
python manage.py inspectdb > models.py
```

反向创建的 Model 类中包含元数据

```
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
