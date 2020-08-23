# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class MaoyanPipeline:
    def process_item(self, item, spider):

        # 保存电影信息到 cvs 文件
        pd_obj = pd.DataFrame(data=[item.values()])
        pd_obj.to_csv('./movies_top10.csv', mode='a+',
                      encoding='utf8', index=False, header=False)

        return item
