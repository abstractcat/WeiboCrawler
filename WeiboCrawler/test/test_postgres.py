# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

import unittest
from WeiboCrawler.postgres import PostgresConn

class TestPostgres(unittest.TestCase):

    def test_insert(self):
        mid='1234567890abcdef'
        uid='1234567890'
        content='test'
        sql = 'insert into weibo(mid,uid,content) values(%s,%s,%s);'
        db=PostgresConn()
        db.execute(sql,(mid,uid,content))

if __name__ == '__main__':
    unittest.main()