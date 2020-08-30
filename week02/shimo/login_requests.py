import requests
from fake_useragent import FakeUserAgent

login_account = input('请您输入登录账号：')
login_password = input('请您输入密码：')

# 登录请求地址
login_url = 'https://shimo.im/lizard-api/auth/password/login'

# 随机获取 User-Agent
ua = FakeUserAgent(verify_ssl=False)
user_agent = ua.random
# print(user_agent)

# 保持会话，请求登录页面
r = requests.Session()

# 请求 headers
headers = {
    'user-agent': user_agent,
    'referer': 'https://shimo.im/login?from=home',
    'origin': 'https://shimo.im',
    'x-requested-with': 'XmlHttpRequest',
    'x-source': 'lizard-desktop'
}

# 请求参数
params = {
    'mobile': f'+86{login_account}',
    'password': login_password
}

post_res = r.post(login_url, data=params, headers=headers)
print(post_res.status_code)
print(post_res.content)
