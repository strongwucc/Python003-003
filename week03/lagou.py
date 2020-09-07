import requests
from selenium import webdriver
import time
import math
import threading
import pymysql
import queue

# 获取职位信息
class CrawlPositions(threading.Thread):
    def __init__(self, position_queue, conn_lock, url, city_name, job_title, limit=100):
        super().__init__()
        self.position_queue = position_queue
        self.conn_lock = conn_lock
        self.city_name = city_name
        self.job_title = job_title
        self.limit = limit
        self.url = url

    def run(self):
        try:
            # 模拟一个谷歌浏览器
            browser = webdriver.Chrome()
            browser.get(self.url)

            # 选择城市
            try:
                change_city_box = browser.find_element_by_xpath('//div[@id="changeCityBox"]')
                time.sleep(1)
                change_city_box.find_element_by_xpath(f'//ul[@class="clearfix"]//a[@data-city="{self.city_name}"]').click()

            except Exception as ex:
                print(f'城市选择失败：{ex}')
            
            # 搜索职位
            search_container = browser.find_element_by_xpath('//div[@id="search_box"]')
            search_container.find_element_by_xpath('//input[@id="search_input"]').send_keys(self.job_title)
            time.sleep(1)
            search_container.find_element_by_xpath('//input[@id="search_button"]').click()

            # 获取职位信息
            pager = 1
            while pager <= math.ceil(self.limit / 15):

                if pager == 1:
                    # 是否有 showData，有就关闭
                    try:
                        browser.find_element_by_xpath('//div[contains(@class, "showData")]//div[@class="body-btn"]').click()
                    except Exception as ex:
                        print(f'showData 选择失败：{ex}')

                # 获取当前页的职位信息
                position_lis = browser.find_elements_by_xpath('//div[@id="s_position_list"]/ul/li')
                with self.conn_lock:
                    for position_li in position_lis:
                        position_name = position_li.get_attribute('data-positionname')
                        position_salary = position_li.get_attribute('data-salary')
                        self.position_queue.put({'city': self.city_name, 'name': position_name, 'salary': position_salary})
                    self.conn_lock.notify_all()

                # 下一页
                print('翻页啦')
                browser.find_element_by_xpath('//*[@id="s_position_list"]/div[2]/div/span[@action="next"]').click()
                time.sleep(2)
                pager += 1
            
        except Exception as e:
            print(f'哎呀，出错啦：{e}')
            return False
        finally:
            print('获取职位信息结束')
            browser.close()

# 保存职位信息
class SavePositions(threading.Thread):
    def __init__(self, position_queue, conn_lock, db):
        super().__init__()
        self.position_queue = position_queue
        self.db = db
        self.conn_lock = conn_lock

    def run(self):

        while True:
            with self.conn_lock:
                if self.position_queue.empty():
                    self.conn_lock.wait()
                else:
                    with self.db.cursor() as cursor:
                        position = self.position_queue.get()
                        try:
                            sql = "INSERT INTO `positions` (`city`, `name`, `salary`) VALUES (%s, %s, %s)"
                            cursor.execute(sql, tuple(position.values()))
                        except Exception as e:
                            self.db.rollback()
                            print(f'数据库写入失败：{e}')
                    self.db.commit()

if __name__ == "__main__":
    lagou_url = 'https://www.lagou.com/'

    # 创建条件锁
    conn_lock = threading.Condition()

    # 创建队列用于保存数据
    position_queue = queue.Queue()

    # 城市列表
    cities = ["北京", "上海", "广州", "深圳"]

    # 开启多线程获取职位信息
    for city in cities:
        crawl_thread = CrawlPositions(position_queue=position_queue, conn_lock=conn_lock,url=lagou_url,city_name=city,job_title="Python 工程师")
        crawl_thread.start()

    # 创建数据库连接
    db_conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='lagou', charset='utf8mb4')

    # 开启多线程保存职位信息
    save_threads = [SavePositions(position_queue=position_queue,conn_lock=conn_lock, db=db_conn) for _ in range(2)]
    for save_thread in save_threads:
        save_thread.start()

    for save_thread in save_threads:
        save_thread.join()

    # 关闭数据库连接
    db_conn.close()