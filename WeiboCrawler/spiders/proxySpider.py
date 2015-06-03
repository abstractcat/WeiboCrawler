# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

from scrapy.spider import Spider
from scrapy.spider import Request
from WeiboCrawler.utils.postgres import PostgresConn
import PyV8

class ProxySpider(Spider):
    def __init__(self):
        self.db = PostgresConn()

    name = "proxy"
    allowed_domains = ['www.site-digger.com']

    def start_requests(self):
        url_sitedigger='http://www.site-digger.com/html/articles/20110516/proxieslist.html'
        print(url_sitedigger)
        yield Request(url=url_sitedigger,callback=self.parse_sitedigger)

    #parse page with splinter
    def parse_sitedigger(self,response):
        sql='INSERT INTO proxy values(%s);'
        ctxt=PyV8.JSContext()
        ctxt.enter()
        script=open('resources/aes.js').read()
        ctxt.eval(script)
        script=open('resources/pad-zeropadding.js').read()
        ctxt.eval(script)

        encrypt_ips=response.xpath('//script/text()').re('document.write\(decrypt\("(.*?)"\)\)')
        for code in encrypt_ips:
            ip=ctxt.eval('decrypt("%s")'%code)
            self.db.execute_param(sql,(ip,))
            print(ip)
