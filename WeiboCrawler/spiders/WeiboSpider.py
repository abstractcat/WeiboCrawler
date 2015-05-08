# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

import cookielib
import json
import re
from datetime import datetime

from scrapy.spider import Spider
from scrapy.http import Request
from scrapy import Selector

from WeiboCrawler import constants
from WeiboCrawler.items import WeiboItem
from WeiboCrawler.login import login


class WeiboSpider(Spider):
    '''
    Crawl weibo list for user given pid and time range.
    '''
    name = "weibo"
    allowed_domains = ['weibo.com', 'sina.com.cn']

    def __init__(self, pid, start, end):
        self.pid = pid
        self.start = start
        self.end = end

    def start_requests(self):
        '''
        Login and crawl weibo for user pid and time range.
        :return:
        '''
        if login(constants.name, constants.pwd, constants.cookie):
            self.login_cookie = read_cookie(constants.cookie)
            print('Login Succeed.')
        else:
            print('Login Failed.')
            return

        page = 1
        section = 1
        crawled = 0
        params = {'pid': self.pid, 'start': self.start, 'end': self.end, 'page': page, 'section': section,
                  'crawled': crawled}
        mblog_list_url = get_mbloglist_url(self.pid, self.start, self.end, page, section)
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
        mblog_div_list = sel.xpath('//div[@action-type="feed_list_item"]').extract()
        section_crawled = len(mblog_div_list)
        print('Number of mblogs in page %s, section %s is: %s' % (params['page'], params['section'], section_crawled))
        params['crawled'] += section_crawled

        # Parse mblog divs and get mblog values.
        mblog_value_list = map(lambda div: parse_mblog_div(div), mblog_div_list)
        for mblog in mblog_value_list:
            yield WeiboItem(mid=mblog[0], uid=mblog[1], content=mblog[2], tm=mblog[3], repost_num=mblog[4],
                            comment_num=mblog[5], like_num=mblog[6])

        # Check if has next page.
        if section_crawled > 0 and params['crawled'] < params['total']:
            if params['section'] < 3:
                params['section'] += 1
            else:
                params['page'] += 1
                params['section'] = 1
            mblog_list_url = get_mbloglist_url(params['pid'], params['start'], params['end'], params['page'],
                                               params['section'])

            yield Request(url=mblog_list_url, cookies=self.login_cookie, callback=self.parse_mblog_list, meta=params)
        else:
            print('Total number of mblogs crawled is: %s' % params['crawled'])


def get_mbloglist_url(pid, start, end, page, section):
    mbloglist_url = 'http://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&is_search=1&is_ori=1&is_pic=1&is_video=1&is_music=1&is_text=1&id=%s&start_time=%s&end_time=%s&page=%s&pre_page=%s&pagebar=%s'
    if section == 1:
        (pre_page, page_bar) = (0, 0)
    elif section == 2:
        (pre_page, page_bar) = (page, 0)
    elif section == 3:
        (pre_page, page_bar) = (page, 1)
    return mbloglist_url % (pid, start, end, page, pre_page, page_bar)


def read_cookie(cookie_file):
    cookie_jar = cookielib.LWPCookieJar(cookie_file)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    cookie = dict()
    for ck in cookie_jar:
        cookie[ck.name] = ck.value
    return cookie


def parse_mblog_div(div):
    sel = Selector(text=div)

    mid = sel.xpath('//div[@action-type="feed_list_item"]/@mid').extract()[0]
    uid = sel.xpath('//div[@action-type="feed_list_item"]/@tbinfo').extract()[0]
    content = sel.xpath('//div[@node-type="feed_list_content"]').extract()[0]
    tm = sel.xpath('//div[@class="WB_from S_txt2"]/a/@date').extract()[0]
    repost_num = sel.xpath('//span[@node-type="forward_btn_text"]/text()').extract()[0]
    comment_num = sel.xpath('//span[@node-type="comment_btn_text"]/text()').extract()[0]
    like_num = sel.xpath('//span[@node-type="like_status"]/em/text()').extract()[0]

    uid = uid.split('=')[1]
    content = re.match(r'<div.*?>(.*)</div>', content.replace('\n', '')).group(1).strip()
    tm = datetime.fromtimestamp(long(tm) / 1000)
    repost_num = int(repost_num.split(' ')[-1])
    comment_num = int(comment_num.split(' ')[-1])
    like_num = int(like_num)

    return (mid, uid, content, tm, repost_num, comment_num, like_num)
