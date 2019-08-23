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

BOT_NAME = 'junyang_spider'

SPIDER_MODULES = ['junyang_spider.spiders']
NEWSPIDER_MODULE = 'junyang_spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'junyang_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Host': 'search.51job.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'junyang_spider.middlewares.JunyangSpiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'junyang_spider.middlewares.JunyangSpiderDownloaderMiddleware': 543,
# }

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
    'junyang_spider.pipelines.MongoPipeline': 200,
    'junyang_spider.pipelines.MysqlPipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline': 300,
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
ENV = "dev"
if ENV == "dev":
    MYSQL_HOST = 'localhost'
    MYSQL_DBNAME = '51job'
    MYSQL_USER = 'root'
    MYSQL_PASSWD = 'qwerty'
    MYSQL_PORT = 3306
    MONGO_URI = "mongodb://root:{pwd}@39.104.185.107:27017/".format(pwd=quote_plus("luoziming@2019!"))
    MONGO_DATABASE = '51Job'
else:
    # online
    MYSQL_HOST = 'rm-hp384ht74xir31xdazo.mysql.huhehaote.rds.aliyuncs.com'
    MYSQL_DBNAME = '51job'
    MYSQL_USER = 'job51'
    MYSQL_PASSWD = '65jaF6vSZUAd20sD'
    MYSQL_PORT = 3306
    MONGO_URI = "mongodb://root:{pwd}@39.104.185.107:27017/".format(pwd=quote_plus("luoziming@2019!"))
    MONGO_DATABASE = '51Job'
