# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem


class MaoyanPipeline:
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
        

    def close_spider(self, spider):
        try:
            self.cursor.close()
            self.client.commit()
            self.client.close()
        except Exception as e:
            raise DropItem(f'MySQL 断开失败：{e}')
        

    def process_item(self, item, spider):
        
        try:
            sql = "INSERT INTO `movies` (`name`, `type`, `time`) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, tuple(item.values()))
        except Exception as e:
            self.client.rollback()
            print(f'数据库写入失败：{e}')

        return item
