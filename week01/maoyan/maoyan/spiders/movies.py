import scrapy
from scrapy.selector import Selector
from maoyan.items import MaoyanItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    # def parse(self, response):
    #     pass

    # 请求域名
    base_url = 'https://maoyan.com'

    # cookie
    cookies_str = '''__mta=50223641.1598148048704.1598196049395.1598196247080.14; uuid_n_v=v1; uuid=7613FFC0E4E411EA889B03421EF8D91B8DD52FDDAF814F879470B04FD1C97AB7; _csrf=ab3d8a12dcff38ad4f93fabc2e9e352087e024f4c3ce86602b36853e5e310788; _lxsdk_cuid=174190bf6fdc8-03e85875010cfe-31617402-1aeaa0-174190bf6fdc8; _lxsdk=7613FFC0E4E411EA889B03421EF8D91B8DD52FDDAF814F879470B04FD1C97AB7; mojo-uuid=2d504596e8d282b7828eb8f1121a71e9; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1598148049,1598148062,1598148093,1598148733; mojo-session-id={"id":"6f9e6bad52bb641edaea9391f4c240ce","time":1598195782997}; __mta=50223641.1598148048704.1598191128330.1598195783166.13; mojo-trace-id=3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1598196247; _lxsdk_s=1741be44fd4-777-ac3-c1a%7C%7C6'''

    # 将字符串的 cookie 转换成字典
    def format_cookies(self):
        return {item.split('=')[0]: item.split('=')[1] for item in self.cookies_str.split('; ')}

    # 起始请求
    def start_requests(self):
        url = f'{self.base_url}/films?showType=3&offset=0'
        cookies = self.format_cookies()
        cookies = {}
        yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    # 列表页解析方法
    def parse(self, response):
        xpath_obj = Selector(response=response)
        # 获取电影详情页面链接
        hrefs = xpath_obj.xpath('//div[@class="movie-item-hover"]//a/@href')
        # print(href.extract_first())
        # 请求 top10 的详情页面
        offset = 0
        for href in hrefs.extract():
            if offset >= 10:
                break
            yield scrapy.Request(url=self.base_url+href, callback=self.parse_detail)
            offset += 1

    # 详情页解析方法
    def parse_detail(self, response):
        info_xpath = Selector(response=response).xpath(
            '//div[@class="movie-brief-container"]')
        # 电影名称
        movie_name = info_xpath.xpath(
            './h1[@class="name"]/text()').extract_first()
        # 电影类型
        movie_type_list = info_xpath.xpath(
            '//li[@class="ellipsis"][1]/a/text()').extract()
        movie_type = '/'.join([movie_type_item.strip()
                               for movie_type_item in movie_type_list])
        # 上映日期
        movie_time = info_xpath.xpath(
            '//li[@class="ellipsis"][3]/text()').extract_first()

        item = MaoyanItem()
        item['movie_name'] = movie_name
        item['movie_type'] = movie_type
        item['movie_time'] = movie_time

        yield item
        # print(f'电影名称：{movie_name}')
        # print(f'类型：{movie_type}')
        # print(f'上映时间：{movie_time}')
