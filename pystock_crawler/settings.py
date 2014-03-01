# Scrapy settings for pystock-crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'pystock-crawler'

SPIDER_MODULES = ['pystock_crawler.spiders']
NEWSPIDER_MODULE = 'pystock_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stockcrawler (+http://www.yourdomain.com)'

LOG_LEVEL = 'INFO'

HTTPCACHE_ENABLED = True

HTTPCACHE_POLICY = 'scrapy.contrib.httpcache.RFC2616Policy'
