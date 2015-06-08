# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

import json
import re
import urlparse
from datetime import datetime

from scrapy.spider import Spider

from scrapy.http import Request

from scrapy import Selector

from abstractcat.db import postgres
from abstractcat.login import entry
from WeiboCrawler.items import WeiboItem


class RetrySpider(Spider):
    '''
    Crawl weibo list for user given pid and time range.
    '''
    name = "retry"
    allowed_domains = ['weibo.com', 'sina.com.cn']

    def __init__(self):
        self.db = postgres.PostgresConn()
        self.entry_manager = entry.EntryManager()

    def start_requests(self):
        '''
        Login and crawl weibo for user pid and time range.
        :return:
        '''

        sql = 'SELECT * from retry;'
        sql_del='DELETE FROM retry WHERE url=\'%s\';'
        urls = map(lambda x:x[0],self.db.query(sql))
        for url in urls:

            parsed_params = urlparse.parse_qs(url)
            page = int(parsed_params['page'][0])
            pid = parsed_params['id'][0]
            start = parsed_params['start_time'][0]
            end = parsed_params['end_time'][0]
            pre_page = int(parsed_params['pre_page'][0])
            page_bar = int(parsed_params['pagebar'][0])
            if (pre_page, page_bar) == (0, 0):
                section = 1
            elif (pre_page, page_bar) == (page, 0):
                section = 2
            else:
                section = 3

            #delete from retry
            self.db.execute(sql_del%url)

            params = {'page': page, 'section': section, 'pid': pid, 'start': start, 'end': end}
            search_url = get_search_url(pid, start, end, page, section)
            cookie = eval(self.entry_manager.get_random_entry()[2])
            yield Request(url=search_url, cookies=cookie, callback=self.search_weibo, errback=self.save_search_url, meta=params)

    def save_search_url(self, response):
        url = response.request.url
        print('error request %s saved!' % url)
        sql = 'INSERT INTO retry values(%s);'
        self.db.execute_param(sql, (url,))

    def search_weibo(self, response):

        print(response.url)
        params = response.meta

        print params

        page = params['page']
        section = params['section']
        pid = params['pid']
        start = params['start']
        end = params['end']

        json_data = json.loads(response.body)
        html = json_data['data']
        sel = Selector(text=html)

        # parse page
        weibo_list = sel.xpath('//div[@action-type="feed_list_item"]').extract()
        weibo_list = map(lambda div: parse_mblog_div(div), weibo_list)
        print 'crawled %s weibo in page %s, section %s' % (len(weibo_list), page, section)

        if len(weibo_list) == 0:
            self.save_search_url(response)
            return

        for weibo in weibo_list:
            (mid, uid, content, tm, repost_num, comment_num, like_num) = weibo
            yield WeiboItem(mid=mid, uid=uid, content=content, tm=tm, repost_num=repost_num, comment_num=comment_num,
                            like_num=like_num)

        # Get total number of mblog from search result
        if page == 1 and section == 1:
            total = int(sel.xpath('//em[@class="W_fb S_spetxt"]/text()').extract()[0].strip())
            print('Total number of mblogs searched is: %s' % total)

            # number of pages left
            num_page = total / 15
            # print(num_page)

            for i in range(num_page):
                if section < 3:
                    section += 1
                else:
                    page += 1
                    section = 1
                search_url = get_search_url(pid, start, end, page, section)
                cookie = eval(self.entry_manager.get_random_entry()[2])
                params['page'] = page
                params['section'] = section
                yield Request(url=search_url, cookies=cookie, callback=self.search_weibo, errback=self.save_search_url,
                              meta=params)


def get_search_url(pid, start, end, page, section):
    search_url = 'http://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&is_search=1&is_ori=1&is_pic=1&is_video=1&is_music=1&is_text=1&id=%s&start_time=%s&end_time=%s&page=%s&pre_page=%s&pagebar=%s'
    if section == 1:
        (pre_page, page_bar) = (0, 0)
    elif section == 2:
        (pre_page, page_bar) = (page, 0)
    elif section == 3:
        (pre_page, page_bar) = (page, 1)
    return search_url % (pid, start, end, page, pre_page, page_bar)


def parse_mblog_div(div):
    sel = Selector(text=div)

    mid = sel.xpath('//div[@action-type="feed_list_item"]/@mid').extract()[0]
    uid = sel.xpath('//div[@action-type="feed_list_item"]/@tbinfo').extract()[0]
    content = sel.xpath('//div[@node-type="feed_list_content"]').extract()[0]
    tm = sel.xpath('//div[@class="WB_from S_txt2"]/a/@date').extract()[0]

    uid = uid.split('=')[1]
    content = re.match(r'<div.*?>(.*)</div>', content.replace('\n', '')).group(1).strip()
    tm = datetime.fromtimestamp(long(tm) / 1000)

    try:
        repost_num = sel.xpath('//span[@node-type="forward_btn_text"]/text()').extract()[0]
        repost_num = int(repost_num.split(' ')[-1])
    except:
        repost_num = 0

    try:
        comment_num = sel.xpath('//span[@node-type="comment_btn_text"]/text()').extract()[0]
        comment_num = int(comment_num.split(' ')[-1])
    except:
        comment_num = 0

    try:
        like_num = sel.xpath('//span[@node-type="like_status"]/em/text()').extract()[0]
        like_num = int(like_num)
    except:
        like_num = 0

    return (mid, uid, content, tm, repost_num, comment_num, like_num)
