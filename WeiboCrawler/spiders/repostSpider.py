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
from WeiboCrawler.items import RepostItem


class RepostSpider(Spider):
    def __init__(self, mid):
        self.mid = mid

    name = "repost"
    allowed_domains = ['weibo.com', 'sina.com.cn']

    def start_requests(self):
        '''
        Login and crawl repost for weibo given mid.
        :return:
        '''
        if login(constants.name, constants.pwd, constants.cookie):
            self.login_cookie = read_cookie(constants.cookie)
            print('Login Succeed.')
        else:
            print('Login Failed.')
            return

        page = 53
        crawled = 0
        params = {'mid': self.mid, 'page': page, 'crawled': crawled}
        repost_list_url = get_repostlist_url(self.mid, page)
        yield Request(url=repost_list_url, cookies=self.login_cookie, callback=self.parse_repost_list, meta=params)


    def parse_repost_list(self, response):
        params = response.meta
        json_data = json.loads(response.body)
        html = json_data['data']['html']
        sel = Selector(text=html)

        # Get total number of pages for reposts.
        if 'totalpage' not in params:
            totalpage = int(json_data['data']['page']['totalpage'])
            params['totalpage'] = totalpage
            print('Total number of repost pages is: %s' % totalpage)

        # Get number of reposts in current page,update meta name 'crawled'.
        repost_div_list = sel.xpath('//div[@action-type="feed_list_item"]').extract()
        page_crawled = len(repost_div_list)
        print('Number of reposts in page %s is: %s' % (params['page'], page_crawled))
        params['crawled'] += page_crawled

        # Parse repost divs and get repost values.
        repost_value_list = map(lambda div: parse_repost_div(div), repost_div_list)
        for repost in repost_value_list:
            yield RepostItem(root_mid=params['mid'], repost_mid=repost[0], uid=repost[1], uname=repost[2],
                             content=repost[3],
                             tm=repost[4], repost_num=repost[5], comment_num=0, like_num=repost[6])

        # Check if has next page.
        if params['page'] < params['totalpage']:
            params['page'] += 1
            repost_list_url = get_repostlist_url(params['mid'], params['page'])

            yield Request(url=repost_list_url, cookies=self.login_cookie, callback=self.parse_repost_list, meta=params)
        else:
            print('Total number of reposts crawled is: %s' % params['crawled'])


def get_repostlist_url(mid, page):
    repostlist_url = 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=%s&page=%s'
    return repostlist_url % (mid, page)


def read_cookie(cookie_file):
    cookie_jar = cookielib.LWPCookieJar(cookie_file)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    cookie = dict()
    for ck in cookie_jar:
        cookie[ck.name] = ck.value
    return cookie


def parse_repost_div(div):
    sel = Selector(text=div)

    repost_mid = sel.xpath('//div[@action-type="feed_list_item"]/@mid').extract()[0]
    uid = sel.xpath('//a[@node-type="name"]/@usercard').extract()[0]
    uname = sel.xpath('//a[@node-type="name"]/text()').extract()[0]
    content = sel.xpath('//span[@node-type="text"]').extract()[0]
    tm = sel.xpath('//div[@class="WB_from S_txt2"]/a/@date').extract()[0]
    repost_num = sel.xpath('//a[@action-type="feed_list_forward"]/text()').extract()[0]

    uid = uid.split('=')[1]
    content = re.match(r'<span.*?>(.*)</span>', content.replace('\n', '')).group(1).strip()
    tm = datetime.fromtimestamp(long(tm) / 1000)
    try:
        repost_num = int(repost_num.split(' ')[-1])
    except:
        repost_num = 0
    try:
        like_num = sel.xpath('//span[@node-type="like_status"]/em/text()').extract()[0]
        like_num = int(like_num)
    except:
        like_num = 0

    return (repost_mid, uid, uname, content, tm, repost_num, like_num)
