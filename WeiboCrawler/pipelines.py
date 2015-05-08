# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from WeiboCrawler.postgres import PostgresConn

class WeiboCrawlerPipeline(object):
    def __init__(self):
        self.db=PostgresConn()

    def process_item(self, item, spider):
        if type(item).__name__=='WeiboItem':
            self.process_weibo_item(item)

    def process_weibo_item(self, item):
        sql = 'INSERT INTO weibo(mid, uid, content, tm, repost_num, comment_num, like_num) values(%s, %s, %s, %s, %s, %s, %s);'
        mid=item['mid']
        uid=item['uid']
        content=item['content']
        tm = item['tm']
        repost_num = item['repost_num']
        comment_num = item['comment_num']
        like_num = item['like_num']
        self.db.execute(sql, (mid, uid, content, tm, repost_num, comment_num, like_num))

