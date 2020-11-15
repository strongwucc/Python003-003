# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from backend.models import Mobile, Comment


class MobileItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = Mobile


class CommentItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = Comment
