from pystock_crawler.spiders.yahoo import YahooSpider
from pystock_crawler.tests.base import TestCaseBase


class YahooSpiderTest(TestCaseBase):

    def test_empty_creation(self):
        spider = YahooSpider()
        self.assertEqual(spider.start_urls, [])

    # TODO: more tests
