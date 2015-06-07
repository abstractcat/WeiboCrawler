# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from  WeiboCrawler.spiders import weiboSpider

def read_uid_list(path):
    userid = []
    f = open(path)
    for line in f:
        userid.append(line.strip())
    return userid

def main():
    uid_list = read_uid_list('E:/PyCharm/CatPackages/resources/doc/user_500.txt')
    print(uid_list)
    spider = weiboSpider.WeiboSpider(uid_list, start='2015-04-15', end='2015-04-20')

    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start_from_crawler(crawler)
    reactor.run()


if __name__ == '__main__':
    main()
    '''
    sql='SELECT * from retry;'
    from abstractcat.db import postgres
    db=postgres.PostgresConn()
    result=db.query(sql)
    print(len(result))
    for r in result:
        print(r[0])
    '''
