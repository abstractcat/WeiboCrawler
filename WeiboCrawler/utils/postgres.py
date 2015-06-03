# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

import psycopg2


class PostgresConn():
    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname=weibo user=postgres host=localhost password=123")
        except Exception as e:
            print 'Failed to connect to database!'
            print 'Error info:',e

    def execute_param(self, sql, param):
        """
        Execute statements with parameters.
        :param sql:
        :param param:
        :return:
        """
        success=True
        cur = self.conn.cursor()
        try:
            cur.execute(sql, param)
            self.conn.commit()
        except Exception as e:
            print 'Failed to execute function execute_param()!'
            print 'Error info:', e.message.decode('utf-8')
            success=False
            self.conn.rollback()
        finally:
            cur.close()
            return success

    def execute(self, sql):
        """
        Execute statements without parameters.
        :param sql:
        :return:
        """
        success=True
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print 'Failed to execute function execute()!'
            print 'Error info:', e.message.decode('utf-8')
            success=False
            self.conn.rollback()
        finally:
            cur.close()
            return success

    def query(self, sql):
        """
        Execute query without parameters.
        :param sql:
        :return:
        """
        result=[]
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            result = cur.fetchall()
        except Exception as e:
            print 'Failed to execute function execute()!'
            print 'Error info:', e.message.decode('utf-8')
            self.conn.rollback()
        finally:
            cur.close()
            return result
