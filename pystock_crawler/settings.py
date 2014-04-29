# Scrapy settings for pystock-crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'pystock-crawler'

EXPORT_FIELDS = (
    # Price columns
    'symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close',

    # Report columns
    'end_date', 'amend', 'period_focus', 'doc_type', 'revenues', 'op_income', 'net_income',
    'eps_basic', 'eps_diluted', 'dividend', 'assets', 'cur_assets', 'cur_liab', 'cash', 'equity',
    'cash_flow_op', 'cash_flow_inv', 'cash_flow_fin',
)

FEED_EXPORTERS = {
    'csv': 'pystock_crawler.exporters.CsvItemExporter2'
}

HTTPCACHE_ENABLED = True

HTTPCACHE_POLICY = 'scrapy.contrib.httpcache.RFC2616Policy'

HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.DbmCacheStorage'

LOG_LEVEL = 'INFO'

NEWSPIDER_MODULE = 'pystock_crawler.spiders'

SPIDER_MODULES = ['pystock_crawler.spiders']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pystock-crawler (+http://www.yourdomain.com)'
