from stockcrawler.spiders.yahoo import YahooSpider
from stockcrawler.tests.base import TestCaseBase


class YahooSpiderTest(TestCaseBase):

    def test_empty_creation(self):
        spider = YahooSpider()
        self.assertEqual(spider.start_urls, [])

    # TODO: more tests
