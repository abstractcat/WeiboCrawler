# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

import unittest

from WeiboCrawler.postgres import PostgresConn


class TestPostgres(unittest.TestCase):
    def test_exec_param(self):
        mid='1234567890abcdef'
        uid='1234567890'
        content='test'
        sql = 'insert into weibo(mid,uid,content) values(%s,%s,%s);'
        db=PostgresConn()
        db.execute_param(sql, (mid, uid, content))

    def test_exec(self):
        mid = '1234567890abcdef'
        sql = "delete from weibo where mid='%s';" % mid
        db = PostgresConn()
        db.execute(sql)

    def test_query(self):
        mid = "3826509582586715"
        sql = "select content from weibo where mid='3826509582586715';"
        db = PostgresConn()
        rows = db.query(sql)
        print(rows[0][0])

if __name__ == '__main__':
    unittest.main()