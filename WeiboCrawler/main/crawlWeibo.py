# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from WeiboCrawler.spiders.weiboSpider import WeiboSpider


def main():
    spider = WeiboSpider(pid='1005051788911247', start='2015-03-01', end='2015-03-31')

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