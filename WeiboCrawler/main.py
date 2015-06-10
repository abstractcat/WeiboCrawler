# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from  WeiboCrawler.spiders import weiboSpider, retrySpider


def read_uid_list(path):
    userid = []
    f = open(path)
    for line in f:
        userid.append(line.strip())
    return userid


def run_weibo_spider():
    uid_list = read_uid_list('E:/PyCharm/CatPackages/resources/doc/user_500.txt')
    print(uid_list)
    spider = weiboSpider.WeiboSpider(uid_list, start='2015-03-15', end='2015-04-15')

    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start_from_crawler(crawler)
    reactor.run()


def run_retry_spider():
    spider = retrySpider.RetrySpider()

    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start_from_crawler(crawler)
    reactor.run()


def main():
    run_weibo_spider()
    #run_retry_spider()


if __name__ == '__main__':
    main()
