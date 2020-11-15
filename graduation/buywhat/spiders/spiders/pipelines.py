# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from scrapy.exceptions import DropItem
from spiders.items import MobileItem, CommentItem
from backend.models import Mobile


class SpidersPipeline:

    def __init__(self, mysql_settings=None):
        self.mysql_settings = mysql_settings

    @classmethod
    def from_crawler(cls, crawler):

        if not crawler.settings.get('MYSQL_SETTINGS'):
            raise DropItem("缺少MySQL的配置")

        return cls(
            mysql_settings=crawler.settings.get('MYSQL_SETTINGS'),
        )

    def open_spider(self, spider):
        try:
            self.client = pymysql.connect(
                host=self.mysql_settings['host'],
                port=self.mysql_settings['port'],
                user=self.mysql_settings['user'],
                password=self.mysql_settings['password'],
                db=self.mysql_settings['db'],
                charset=self.mysql_settings['charset']
            )
        except Exception as e:
            raise DropItem(f'MySQL 连接失败：{e}')

        self.cursor = self.client.cursor()

        # 清空数据库
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.cursor.execute("TRUNCATE TABLE backend_comment")
        self.cursor.execute("TRUNCATE TABLE backend_mobile")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        try:
            self.cursor.close()
            self.client.commit()
            self.client.close()
        except Exception as e:
            raise DropItem(f'MySQL 断开失败：{e}')

    def process_item(self, item, spider):

        if isinstance(item, dict):

            mobile = item['mobile']
            comments = item['comments']

            mobile.save()

            print(mobile['name'])

            for comment in comments:
                comment['mobile'] = Mobile.objects.get(name=mobile['name'])
                comment['sentiment'] = 0
                comment.save()

            # return item
