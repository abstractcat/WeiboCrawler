# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from abstractcat.db import postgres


class WeiboCrawlerPipeline(object):
    def __init__(self):
        self.db = postgres.PostgresConn()

    def process_item(self, item, spider):
        sql = 'INSERT INTO weibo(mid, uid, content, tm, repost_num, comment_num, like_num) values(%s, %s, %s, %s, %s, %s, %s);'
        mid = item['mid']
        uid = item['uid']
        content = item['content']
        tm = item['tm']
        repost_num = item['repost_num']
        comment_num = item['comment_num']
        like_num = item['like_num']
        self.db.execute_param(sql, (mid, uid, content, tm, repost_num, comment_num, like_num))

    '''
    def process_repost_item(self, item):
        sql = 'INSERT INTO repost(root_mid, repost_mid, uid, uname, content, tm, repost_num, comment_num, like_num) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
        root_mid = item['root_mid']
        repost_mid = item['repost_mid']
        uid = item['uid']
        uname = item['uname']
        content = item['content']
        tm = item['tm']
        repost_num = item['repost_num']
        comment_num = item['comment_num']
        like_num = item['like_num']
        self.db.execute_param(sql, (root_mid, repost_mid, uid, uname, content, tm, repost_num, comment_num, like_num))
    '''