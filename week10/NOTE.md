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
