# Scrapy settings for product project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'product'

SPIDER_MODULES = ['product.spiders']
NEWSPIDER_MODULE = 'product.spiders'
ITEM_PIPELINES = {'product.mysqlstorepipeline.MySQLStorePipeline':300}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'product (+http://www.yourdomain.com)'

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    ]

HTTP_PROXY = 'http://127.0.0.1:8123'

DOWNLOADER_MIDDLEWARES = {
    'product.middlewares.RandomUserAgentMiddleware': 400,
    'product.middlewares.ProxyMiddleware': 410,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

#LOG_ENABLED = False
CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_ITEMS = 200