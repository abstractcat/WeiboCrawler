# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

import psycopg2


class PostgresConn():
    def __init__(self):
        self.conn = psycopg2.connect("dbname=weibo user=postgres host=localhost")

    def execute_param(self, sql, param):
        """
        Execute statements with parameters.
        :param sql:
        :param param:
        :return:
        """
        cur = self.conn.cursor()
        try:
            cur.execute(sql, param)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            cur.close()

    def execute(self, sql):
        """
        Execute statements without parameters.
        :param sql:
        :return:
        """
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            cur.close()

    def query(self, sql):
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

