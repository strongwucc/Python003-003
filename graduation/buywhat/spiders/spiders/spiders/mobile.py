import scrapy
import datetime
import pytz
from scrapy.selector import Selector
from spiders.items import MobileItem, CommentItem
from scrapy import signals
import pandas as pd
from sqlalchemy import create_engine
from snownlp import SnowNLP
from django.conf import settings


class MobileSpider(scrapy.Spider):
    name = 'mobile'
    allowed_domains = ['www.smzdm.com']
    start_urls = ['https://www.smzdm.com']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MobileSpider, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    top = 10

    def start_requests(self):
        # 请求24小时手机排名前10
        # mobiles_url = f'{self.start_urls[0]}/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/'
        mobiles_url = f'{self.start_urls[0]}/fenlei/qipaoshui/h5c4s0f0t0p1/#feed-main/'
        # 发送请求
        yield scrapy.Request(mobiles_url, callback=self.parse_list)

    def parse_list(self, response):
        # 获取前10手机信息
        xpath_obj = Selector(response)
        mobile_objs = xpath_obj.xpath(
            '//ul[@id="feed-main-list"]/li[position()<11]')

        for mobile_obj in mobile_objs:

            # 名称
            name = mobile_obj.xpath(
                './/h5[@class="feed-block-title"]/a/text()').extract_first()

            # 值得购买数量
            worth_n = mobile_obj.xpath(
                './/a[contains(@class,"price-btn-up")]/span[@class="unvoted-wrap"]/span/text()').extract_first()

            # 不值得购买数量
            not_worth_n = mobile_obj.xpath(
                './/a[contains(@class,"price-btn-down")]/span[@class="unvoted-wrap"]/span/text()').extract_first()

            # 评论数
            comment_n = mobile_obj.xpath(
                './/a[@class="z-group-data"]/span/text()').extract_first()

            # 平台
            source = mobile_obj.xpath(
                './/span[@class="feed-block-extras"]/a/text()').extract_first().strip()

            # 详情页地址
            detail_url = mobile_obj.xpath(
                './/h5[@class="feed-block-title"]/a/@href').extract_first()

            # print(detail_url)

            mobile = MobileItem()
            mobile['name'] = name
            mobile['worth_n'] = worth_n
            mobile['not_worth_n'] = not_worth_n
            mobile['comment_n'] = comment_n
            mobile['source'] = source

            comments = []

            yield scrapy.Request(detail_url, callback=lambda response, mobile=mobile, comments=comments: self.parse_detail(response, mobile, comments))

            # yield item

    def parse_detail(self, response, mobile, comments):

        # print(mobile)

        # 获取评论
        xpath_obj = Selector(response)
        comment_objs = xpath_obj.xpath(
            '//ul[@class="comment_listBox"]/li[@class="comment_list"]')

        for comment_obj in comment_objs:
            content = comment_obj.xpath(
                './/span[@itemprop="description"]/text()').extract_first()
            comment_time = comment_obj.xpath(
                './/div[@class="time"]/text()').extract_first()

            tz = pytz.timezone('Asia/Shanghai')
            create_time = datetime.datetime.now(tz)

            if comment_time.find('刚刚') >= 0:
                comment_time = create_time.strftime("%Y-%m-%d %H:%M:%S")
            elif comment_time.find('分钟前') >= 0:
                offset_m = int(comment_time[:comment_time.find('分钟前')])
                comment_time = (create_time + datetime.timedelta(minutes=-offset_m)
                                ).strftime("%Y-%m-%d %H:%M:%S")
            elif comment_time.find('小时前') >= 0:
                offset_h = int(comment_time[:comment_time.find('小时前')])
                comment_time = (create_time + datetime.timedelta(hours=-offset_h)
                                ).strftime("%Y-%m-%d %H:%M:%S")
            else:
                comment_time = datetime.datetime.strptime(create_time.strftime(
                    "%Y-") + comment_time, "%Y-%m-%d %H:%M")

            # print(content, comment_time, comment_time)
            comment = CommentItem()
            comment['content'] = content
            comment['comment_t'] = comment_time
            comment['create_t'] = create_time.strftime("%Y-%m-%d %H:%M:%S")
            comments.append(comment)

        # 判断是否还有下一页
        next_page = xpath_obj.xpath(
            '//ul[@class="pagination"]/li[@class="pagedown"]/a/@href').extract_first()

        # print(next_page, mobile, comments)
        print(next_page)

        if next_page:
            yield scrapy.Request(next_page, callback=lambda response, mobile=mobile: self.parse_detail(response, mobile, comments))
        else:
            item = {'mobile': mobile, 'comments': comments}
            yield item

    def spider_closed(self, spider):
        # spider.logger.info('Spider closed: %s', spider.name)
        
        db_setting = settings.DATABASES['default']
        engine = create_engine(
            f'mysql+pymysql://{db_setting["USER"]}:{db_setting["PASSWORD"]}@{db_setting["HOST"]}:{db_setting["PORT"]}/{db_setting["NAME"]}')

        sql = 'select * from backend_comment;'
        df = pd.read_sql_query(sql, engine)
        df_copy = df.copy()

        # 删除空值
        df_copy = df_copy.dropna()
        # 删除''值
        df_copy = df_copy.drop(df_copy[df_copy.content == ''].index)
        # 评论内容去重
        df_copy = df_copy.drop_duplicates('content')

        # 进行语义情感分析
        df_copy['sentiment'] = df_copy['content'].map(
            lambda x: SnowNLP(x).sentiments)

        # 存入数据库，并设置相关主键
        df_copy.to_sql('backend_comment', engine,
                       if_exists='replace', index=False)
        with engine.connect() as con:
            con.execute(
                'ALTER TABLE backend_comment ADD PRIMARY KEY (`id`);')
            con.execute(
                'ALTER TABLE backend_comment CHANGE id id BIGINT NOT NULL AUTO_INCREMENT;')
