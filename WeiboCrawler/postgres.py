# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

import psycopg2

class PostgresConn():
    def __init__(self):
        self.conn = psycopg2.connect("dbname=weibo user=postgres host=localhost")

    def execute(self, sql, data):
        """
        Execute insert or update statements with parameters.
        :param sql:
        :param data:
        :return:
        """
        cur = self.conn.cursor()
        try:
            cur.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            cur.close()

    def query(self,sql, data):
        """
        Execute query with parameters.
        :param sql:
        :param data:
        :return:
        """
        cur = self.conn.cursor()
        try:
            cur.execute(sql, data)
            rows = cur.fetchall()
            cur.close()
            return rows
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            cur.close()

    def query(self,sql):
        """
        Execute query without parameters.
        :param sql:
        :return:
        """
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            return rows
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            cur.close()

