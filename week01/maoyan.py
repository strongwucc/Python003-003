# 安装并使用 requests、bs4 库，
# 爬取猫眼电影（）的前 10 个电影名称、电影类型和上映时间，
# 并以 UTF-8 字符集保存到 csv 格式的文件中

# 导入 requests 和 bs4 库
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

# 请求链接
url = 'https://maoyan.com/films'

# 请求头
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
headers = {'user-agent': user_agent}

# 设置 cookie
cookies_str = '''__mta=50223641.1598148048704.1598150393012.1598151601514.11; uuid_n_v=v1; uuid=7613FFC0E4E411EA889B03421EF8D91B8DD52FDDAF814F879470B04FD1C97AB7; _csrf=ab3d8a12dcff38ad4f93fabc2e9e352087e024f4c3ce86602b36853e5e310788; _lxsdk_cuid=174190bf6fdc8-03e85875010cfe-31617402-1aeaa0-174190bf6fdc8; _lxsdk=7613FFC0E4E411EA889B03421EF8D91B8DD52FDDAF814F879470B04FD1C97AB7; mojo-uuid=2d504596e8d282b7828eb8f1121a71e9; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1598148049,1598148062,1598148093,1598148733; __mta=50223641.1598148048704.1598150390217.1598150393012.10; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1598151601; _lxsdk_s=174199abfbf-11e-0a2-abb%7C%7C1'''

# 将字符串类型的 cookie 数据转化为字典类型
cookies = {item.split('=')[0]: item.split('=')[1]
           for item in cookies_str.split('; ')}
# print(cookies)


# 请求参数
params = {'showType': 3, 'offset': 0}

# 发起请求并获取请求结果
response = requests.get(url, headers=headers, params=params, cookies=cookies)

# print(response.text)

# 用 BeautifulSoup 对网页进行解析
soup = bs(response.text, 'html.parser')

# 查找电影信息所在的 div
movies = soup.find_all('div', attrs={'class': 'movie-hover-info'})

movies_list = []
offset = 0

# 查找每个电影的信息
for movie in movies:
    # 只查找前 10 个
    if offset >= 10:
        break
    # 获取电影名称
    movie_name = movie.find('span', attrs={'class': 'name'}).get_text().strip()
    # print(name)

    # 电影类型和上映时间
    other_info = movie.find_all('div', attrs={'class': 'movie-hover-title'})
    movie_type = ''
    movie_time = ''

    # 用正则去获取电影类型和上映时间
    for info in other_info:
        regex = r'类型:\s?(.*)|上映时间:\s?(.*)'
        pattern = re.compile(regex, re.DOTALL)
        res = pattern.search(info.get_text())
        if res is not None:
            if res.group(1) is not None:
                movie_type = res.group(1).strip()
            elif res.group(2) is not None:
                movie_time = res.group(2).strip()

    # print(movie_name)
    # print(movie_type)
    # print(movie_time)
    movies_list.append(
        {"电影名称": movie_name, "类型": movie_type, "上映日期": movie_time})
    offset += 1

# 保存到文件
print(movies_list)
pd_obj = pd.DataFrame(data=movies_list)
pd_obj.to_csv('./movies_top10.csv', encoding='utf8', index=False)
