# -*- coding: utf-8 -*-
from datetime import datetime

# Scrapy settings for jsasx project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jsasx'

SPIDER_MODULES = ['jsasx.spiders']
NEWSPIDER_MODULE = 'jsasx.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jsasx (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jsasx.middlewares.JsasxSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'jsasx.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'jsasx.pipelines.SomePipeline': 300,
#}
ITEM_PIPELINES = {
	'scrapy.pipelines.images.ImagesPipeline': 1,
	'jsasx.pipelines.MyImagesPipeline': 2
}
IMAGES_STORE = "downloads"

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Generate log file
LOG_FILE = 'logs/{}.txt'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))

# Proejct setting
API_BASE_URL = "http://jsasx.com/wp-json/wp/v2/"
MEDIA_URL = "http://s1.imagescool.com/wp-json/wp/v2/"
MEDIA_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9zMS5pbWFnZXNjb29sLmNvbSIsImlhdCI6MTQ4Njk3NTI4NSwibmJmIjoxNDg2OTc1Mjg1LCJleHAiOjE0ODc1ODAwODUsImRhdGEiOnsidXNlciI6eyJpZCI6IjEifX19.b7LqdoJ3zg0wSHquFKN9PqD2QpWM3SA7fl9ku956jwE"
UPLOAD_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9qc2FzeC5jb20iLCJpYXQiOjE0ODY5NzU2NjIsIm5iZiI6MTQ4Njk3NTY2MiwiZXhwIjoxNDg3NTgwNDYyLCJkYXRhIjp7InVzZXIiOnsiaWQiOiIxIn19fQ.XKV7nuvLqVPID7ex3juqjJ7jRkthUJfsP4mhKeRtep0"
CATEGORY_LIST = []
DEFAULT_REQUEST_HEADERS = {
	'Referer': ""
}