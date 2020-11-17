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
from django.conf import settings

class SpidersPipeline:

    def __init__(self, mysql_settings=None):
        self.mysql_settings = mysql_settings

    @classmethod
    def from_crawler(cls, crawler):

        if not crawler.settings.get('MYSQL_SETTINGS'):
            raise DropItem("缺少MySQL的配置")

        return cls(
            mysql_settings=settings.DATABASES.get('default'),
        )

    def open_spider(self, spider):
        try:
            self.client = pymysql.connect(
                host=self.mysql_settings['HOST'],
                port=int(self.mysql_settings['PORT']),
                user=self.mysql_settings['USER'],
                password=self.mysql_settings['PASSWORD'],
                db=self.mysql_settings['NAME'],
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

            for comment in comments:
                comment['mobile'] = Mobile.objects.get(name=mobile['name'])
                comment['sentiment'] = 0
                comment.save()

            # return item
