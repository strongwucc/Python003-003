# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from maoyan.items import MaoyanItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com']

    # def parse(self, response):
    #     pass

    # 获取的电影数量
    top = 10
    offset = 0

    def start_requests(self):
        self.offset = 0
        # 请求电影列表页面
        movies_url = f'{self.start_urls[0]}/films?showType=3&offset=0'
        # 发送请求
        yield scrapy.Request(movies_url, callback=self.parse_list)

    def parse_list(self, response):
        # 获取电影详情页面链接
        xpath_obj = Selector(response)
        detail_urls = xpath_obj.xpath('//div[@class="movie-item film-channel"]/a/@href')
        urls = detail_urls.extract()
        for url in urls:
            if self.offset >= self.top:
                break
            yield scrapy.Request(self.start_urls[0] + url, callback=self.parse_detail)
            self.offset += 1

    def parse_detail(self, response):
        # 获取电影信息
        xpath_obj = Selector(response)
        info_obj = xpath_obj.xpath('//div[@class="movie-brief-container"]')
        # 电影名称
        name_obj = info_obj.xpath('./h1[@class="name"]/text()')
        movie_name = name_obj.extract_first()
        # 类型信息
        type_obj = info_obj.xpath('.//li[@class="ellipsis"][1]/a/text()')
        movie_type = '/'.join([ type_value.strip() for type_value in type_obj.extract()])
        # 上映时间
        time_obj = info_obj.xpath('//li[@class="ellipsis"][3]/text()')
        movie_time = time_obj.extract_first()

        item = MaoyanItem()
        item['movie_name'] = movie_name
        item['movie_type'] = movie_type
        item['movie_time'] = movie_time

        yield item