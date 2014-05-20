import logging

from scrapy.exceptions import NotConfigured
from scrapy import signals


class PassiveThrottle(object):
    '''
    Scrapy's AutoThrottle adds too much download delay on edgar spider, making
    it too slow.

    PassiveThrottle takes a more "passive" approach. It adds download delay
    only if there is an error response.

    '''
    def __init__(self, crawler):
        self.crawler = crawler
        if not crawler.settings.getbool('PASSIVETHROTTLE_ENABLED'):
            raise NotConfigured

        self.debug = crawler.settings.getbool("PASSIVETHROTTLE_DEBUG")
        crawler.signals.connect(self._spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(self._response_downloaded, signal=signals.response_downloaded)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def _spider_opened(self, spider):
        self.mindelay = self._min_delay(spider)
        self.maxdelay = self._max_delay(spider)
        self.retry_http_codes = self._retry_http_codes()

    def _min_delay(self, spider):
        s = self.crawler.settings
        return getattr(spider, 'download_delay', 0.0) or \
            s.getfloat('DOWNLOAD_DELAY')

    def _max_delay(self, spider):
        return self.crawler.settings.getfloat('PASSIVETHROTTLE_MAX_DELAY', 60.0)

    def _retry_http_codes(self):
        return self.crawler.settings.getlist('RETRY_HTTP_CODES', [])

    def _response_downloaded(self, response, request, spider):
        key, slot = self._get_slot(request, spider)
        if slot is None:
            return

        olddelay = slot.delay
        self._adjust_delay(slot, response)
        if self.debug:
            diff = slot.delay - olddelay
            conc = len(slot.transferring)
            msg = "slot: %s | conc:%2d | delay:%5d ms (%+d)" % \
                  (key, conc, slot.delay * 1000, diff * 1000)
            spider.log(msg, level=logging.INFO)

    def _get_slot(self, request, spider):
        key = request.meta.get('download_slot')
        return key, self.crawler.engine.downloader.slots.get(key)

    def _adjust_delay(self, slot, response):
        """Define delay adjustment policy"""
        if response.status in self.retry_http_codes:
            new_delay = max(slot.delay, 1) * 4
            new_delay = max(new_delay, self.mindelay)
            new_delay = min(new_delay, self.maxdelay)
            slot.delay = new_delay
        elif response.status == 200:
            new_delay = max(slot.delay / 2, self.mindelay)
            if new_delay < 0.01:
                new_delay = 0
            slot.delay = new_delay
