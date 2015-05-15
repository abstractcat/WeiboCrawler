# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    mid = scrapy.Field()
    uid = scrapy.Field()
    content = scrapy.Field()
    tm = scrapy.Field()
    repost_num = scrapy.Field()
    comment_num = scrapy.Field()
    like_num = scrapy.Field()


class RepostItem(scrapy.Item):
    root_mid = scrapy.Field()
    repost_mid = scrapy.Field()
    uid = scrapy.Field()
    uname = scrapy.Field()
    content = scrapy.Field()
    tm = scrapy.Field()
    repost_num = scrapy.Field()
    comment_num = scrapy.Field()
    like_num = scrapy.Field()