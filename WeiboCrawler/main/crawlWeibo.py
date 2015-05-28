# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from WeiboCrawler.spiders.weiboSpider import WeiboSpider


def read_user_list(path):
    userid=[]
    f=open(path)
    for line in f:
        userid.append(line.strip())
    print(userid)
    return userid

def main():
    userid=read_user_list('../script/user_500.txt')

    spider = WeiboSpider(pid='1006062786930387', start='2015-03-01', end='2015-03-31')

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