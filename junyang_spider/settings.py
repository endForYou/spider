# -*- coding: utf-8 -*-

# Scrapy settings for junyang_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from urllib.parse import quote_plus
import random

BOT_NAME = 'junyang_spider'

SPIDER_MODULES = ['junyang_spider.spiders']
NEWSPIDER_MODULE = 'junyang_spider.spiders'

USER_AGENT_LIST = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    " Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
    " Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",

]
user_agents = random.choice(USER_AGENT_LIST)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
# if user_agents:
#     USER_AGENT = user_agents
# else:
#     USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'junyang_spider (+http://www.yourdomain.com)'
MEDIA_ALLOW_REDIRECTS = True
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.0
# 0.5 * DOWNLOAD_DELAY和1.5 * 之间的随机间隔
RANDOMIZE_DOWNLOAD_DELAY = True

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'UM_distinctid=172c24e1e3b2b5-04f562c4778a47-14396257-fa000-172c24e1e3c8a5; connect.sid=s%3A0XSv9MheyRObTbSNhSynjSfPwiTfH7jZ.ooy6QqQxo30AJfEUg%2FdgmscOS3Efj0beYq8ZqCVUm1I; youzy.pv4y.uid=jbqbd5i/twjRnIo2ofiCog==; youzy.pv4y.type=toC',
    'Content-Type': 'application/json'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'junyang_spider.middlewares.JunyangSpiderSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'junyang_spider.middlewares.JunyangSpiderDownloaderMiddleware': None,
    'junyang_spider.middlewares.JunyangSpiderCustomDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'junyang_spider.pipelines.JunyangSpiderPipeline': 300,
# }
ITEM_PIPELINES = {
    # 'junyang_spider.pipelines.MongoPipeline': 200,
    # 'junyang_spider.pipelines.MysqlPipeline': 300,
    # 'junyang_spider.pipelines.PaperEWTPipeline': 200,
    # 'junyang_spider.pipelines.files.FilesPipeline': 1
    # 'junyang_spider.pipelines.RedisPipeline': 300,
    # 'junyang_spider.pipelines.NcdaPipeline': 300,
    'junyang_spider.pipelines.YzyCollegePipeline': 300,
    'junyang_spider.pipelines.YzyCollegeDetailPipline': 200,
    'junyang_spider.pipelines.YzyCollegeEnrollCodePipline': 100,
    'junyang_spider.pipelines.YzyCollegeScorelinePipline': 100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
REDIS_URL = 'redis://@localhost:6379'
INSERT_LIMIT = 0
# MYSQL_HOST = 'rm-hp384ht74xir31xdazo.mysql.huhehaote.rds.aliyuncs.com'
# MYSQL_DBNAME = '51job'
# MYSQL_USER = 'job51'
# MYSQL_PASSWD = '65jaF6vSZUAd20sD'
# ENV = "pro"
# if ENV == "dev":
#     MYSQL_HOST = 'localhost'
#     MYSQL_DBNAME = '51job'
#     MYSQL_USER = 'root'
#     MYSQL_PASSWD = 'qwerty'
#     MYSQL_PORT = 3306
#     MONGO_URI = "mongodb://root:{pwd}@39.104.185.107:27017/".format(pwd=quote_plus("luoziming@2019!"))
#     MONGO_DATABASE = '51Job'
# else:
# online
# MYSQL_HOST = 'rm-hp384ht74xir31xdazo.mysql.huhehaote.rds.aliyuncs.com'
# MYSQL_DBNAME = '51job'
# MYSQL_USER = 'job51'
# MYSQL_PASSWD = '65jaF6vSZUAd20sD'
# MYSQL_PORT = 3306
# MONGO_URI = "mongodb://root:{pwd}@39.104.185.107:27017/".format(pwd=quote_plus("luoziming@2019!"))
# MONGO_DATABASE = '51Job'
MYSQL_HOST = '39.104.123.45'
MYSQL_DBNAME = 'zhiyuan_new'
MYSQL_USER = 'resource'
MYSQL_PASSWD = "vX1+U4N7HVZaiUhHQkV+oIOyHTw="
MYSQL_PORT = 3306
MYSQL_CHARSET = 'utf8'
# MONGO_URI = "mongodb://root:{pwd}@39.104.185.107:27017/".format(pwd=quote_plus("luoziming@2019!"))
# MONGO_DATABASE = '51Job'
# FILE_STORE = 'D:\\totransfer'
