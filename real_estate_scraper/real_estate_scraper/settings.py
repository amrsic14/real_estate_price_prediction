# Scrapy settings for real_estate_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'real_estate_scraper'

SPIDER_MODULES = ['real_estate_scraper.spiders']
NEWSPIDER_MODULE = 'real_estate_scraper.spiders'

# RETRY_HTTP_CODES = [429]
#
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#     'real_estate_scraper.middlewares.TooManyRequestsRetryMiddleware': 543,
# }

# ROTATING_PROXY_LIST = [
#     # 'https://zluacjuh:u2cr9i6834ls@209.127.191.180:9279',
#     # 'https://zluacjuh:u2cr9i6834ls@45.142.28.83:8094',
#     # 'https://zluacjuh:u2cr9i6834ls@45.95.99.20:7580',
#     # 'https://zluacjuh:u2cr9i6834ls@45.95.96.132:8691',
#     # 'https://zluacjuh:u2cr9i6834ls@45.95.99.226:7786',
#     # 'https://zluacjuh:u2cr9i6834ls@45.95.96.237:8796',
#     # 'https://zluacjuh:u2cr9i6834ls@45.95.96.187:8746',
#     # 'https://zluacjuh:u2cr9i6834ls@193.8.127.189:9271',
#     # 'https://zluacjuh:u2cr9i6834ls@193.8.56.119:9183'
#     'http://38.91.57.43:3128',
#     'http://12.151.56.30:80'
#     'http://88.255.12.25:8080',
#     'http://177.185.94.177:3128',
#     'http://201.140.209.42:3128',
#     'http://128.199.108.29:3128',
#     'http://188.166.124.18:80',
#     'http://98.12.195.129:443',
#     'http://201.184.171.244:999',
#     'http://122.147.254.62:80',
#     'http://114.240.230.242:808',
#     'http://144.22.212.241:8888',
#     'http://221.215.175.211:9999',
#     'http://114.93.186.160:8000',
#     'http://222.178.243.202:10086',
#     'http://110.78.159.34:8080',
#     'http://37.49.230.22:8187',
#     'http://122.192.30.17:8080',
#     'http://218.3.178.14:3128',
#     'http://36.138.54.45:1080',
#     'http://131.255.229.128:8080'
# ]
#
# DOWNLOADER_MIDDLEWARES = {
#     'rotating_proxies.middlewares.RotatingProxyMiddleware': 800,
#     'rotating_proxies.middlewares.BanDetectionMiddleware': 800,
# }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'real_estate_scraper (+http://www.yourdomain.com)'
USER_AGENT="Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
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
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'real_estate_scraper.middlewares.RealEstateScraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'real_estate_scraper.middlewares.RealEstateScraperDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'real_estate_scraper.pipelines.RealEstateScraperPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Retry many times since proxies often fail
RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408, 429]

DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 800,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 800
}

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...
PROXY_LIST = 'proxy_list.txt'

# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
PROXY_MODE = 0
