# 导入 webdriver
from selenium import webdriver

# 石墨文档首页
home_page = 'https://shimo.im/welcome'

login_name = input('请您输入账号：')
password = input('请您输入密码：')

try:
    # 获取 chrome 对象
    chrome = webdriver.Chrome()
    # 打开石墨文档首页
    chrome.get(home_page)

    # 查找登录按钮
    login_btn = chrome.find_element_by_xpath(
        '//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
    # print(login_btn)
    # 模拟点击
    login_btn.click()

    # 获取输入框和立即登录按钮
    mobile_inpput = chrome.find_element_by_xpath(
        '//input[@name="mobileOrEmail"]')
    password_input = chrome.find_element_by_xpath('//input[@name="password"]')
    submit_btn = chrome.find_element_by_xpath(
        '//button[contains(@class, "submit")]')

    # print(mobile_inpput)
    # print(password_input)
    # print(submit_btn)

    # 输入账号密码并点击立即登录
    mobile_inpput.send_keys(login_name)
    password_input.send_keys(password)

    submit_btn.click()

    # 获取登录后的 cookies
    cookies = chrome.get_cookies()
    print(cookies)

except Exception as e:
    print(f'哎呀出错啦：{e}')
finally:
    pass
    # if 'chrome' in locals().keys():
    #     chrome.close()
