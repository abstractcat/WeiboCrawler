# -*- coding: utf-8 -*-

# Scrapy settings for WeiboCrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'WeiboCrawler'

SPIDER_MODULES = ['WeiboCrawler.spiders']
NEWSPIDER_MODULE = 'WeiboCrawler.spiders'
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'DEBUG.log'

DOWNLOAD_DELAY = 1.5

ITEM_PIPELINES = {
    'WeiboCrawler.pipelines.WeiboCrawlerPipeline': 300
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'WeiboCrawler (+http://www.yourdomain.com)'
