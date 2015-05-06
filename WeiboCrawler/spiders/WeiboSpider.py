# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

from scrapy.spider import Spider
from scrapy.http import Request
from scrapy import Selector

import cookielib
import pdb
import json

from WeiboCrawler.login import login


class WeiboSpider(Spider):
    name = "weibo"
    allowed_domains = ['weibo.com', 'sina.com.cn']

    def start_requests(self):
        '''
        Login and crawl weibo for user id and time range.
        :return:
        '''
        name = 'data6paper@sina.com'
        pwd = 'cikm2015'
        cookie = 'weibo_login_cookies.dat'
        if login(name, pwd, cookie):
            self.login_cookie = read_cookie()
        else:
            print('Login Failed.')
            return

        id = '1005051788911247'
        start = '2015-03-01'
        end = '2015-03-31'
        page = 1
        section = 1
        crawled = 0
        params = {'id': id, 'start': start, 'end': end, 'page': page, 'section': section, 'crawled': crawled}
        mblog_list_url = get_mbloglist_url(id, start, end, page, section)
        yield Request(url=mblog_list_url, cookies=self.login_cookie, callback=self.parse_mblog_list, meta=params)


    def parse_mblog_list(self, response):
        params = response.meta
        json_data = json.loads(response.body)
        html = json_data['data']
        sel = Selector(text=html)

        # Get total number of mblog from first page, put it into meta
        if params['page'] == 1 and params['section'] == 1:
            total = int(sel.xpath('//em[@class="W_fb S_spetxt"]/text()').extract()[0].strip())
            params['total'] = total
            print('Total number of mblogs searched is: %s' % total)

        # Get number of mblog for current section, update meta name 'crawled'.
        mblog_list = sel.xpath('//div[@class="WB_detail"]').extract()

        section_crawled = len(mblog_list)
        print('Number of mblogs in page %s, section %s is: %s' % (params['page'], params['section'], section_crawled))
        params['crawled'] += section_crawled

        #Check if has next page.
        if section_crawled>0 and params['crawled'] < params['total']:
            if params['section'] < 3:
                params['section'] += 1
            else:
                params['page'] += 1
                params['section'] = 1
            mblog_list_url = get_mbloglist_url(params['id'], params['start'], params['end'], params['page'],
                                               params['section'])
            return Request(url=mblog_list_url, cookies=self.login_cookie, callback=self.parse_mblog_list, meta=params)
        else:
            print('Total number of mblogs crawled is: %s' % params['crawled'])

def get_mbloglist_url(id, start, end, page, section):
    mbloglist_url = 'http://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&is_search=1&is_ori=1&is_pic=1&is_video=1&is_music=1&is_text=1&id=%s&start_time=%s&end_time=%s&page=%s&pre_page=%s&pagebar=%s'
    if section == 1:
        (pre_page, page_bar) = (0, 0)
    elif section == 2:
        (pre_page, page_bar) = (page, 0)
    elif section == 3:
        (pre_page, page_bar) = (page, 1)
    return mbloglist_url % (id, start, end, page, pre_page, page_bar)

def read_cookie():
    cookie_file = "weibo_login_cookies.dat"
    cookie_jar = cookielib.LWPCookieJar(cookie_file)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    cookie = dict()
    for ck in cookie_jar:
        cookie[ck.name] = ck.value
    return cookie