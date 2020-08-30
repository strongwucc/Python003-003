import requests
from fake_useragent import FakeUserAgent

login_account = input('请您输入登录账号：')
login_password = input('请您输入密码：')

# 登录页面地址
login_page_url = 'https://shimo.im/login?from=home'

# 登录请求地址
login_post_url = 'https://shimo.im/lizard-api/auth/password/login'

# 随机获取 User-Agent
ua = FakeUserAgent(verify_ssl=False)
user_agent = ua.random

# 保持会话，请求登录页面
r = requests.Session()
get_res = r.get(login_page_url, headers={'user-agent': user_agent})
cookies = get_res.cookies
# print(cookies)

# 如果登录页面请求成功，则进行登录请求
if get_res.status_code == 200:

    # 请求 headers
    headers = {
        'user-agent': user_agent,
        'referer': 'https://shimo.im/login?from=home',
        'origin': 'https://shimo.im'
    }

    # 请求参数
    params = {
        'mobile': f'+86{login_account}',
        'password': login_password
    }

    post_res = r.post(login_post_url, data=params,
                      headers=headers, cookies=cookies)
    print(post_res.status_code)
    print(post_res.content)
else:
    print('登录失败')
