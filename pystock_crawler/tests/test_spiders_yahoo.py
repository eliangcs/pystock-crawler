from pystock_crawler.spiders.yahoo import make_url, YahooSpider
from pystock_crawler.tests.base import TestCaseBase


class MakeURLTest(TestCaseBase):

    def test_no_dates(self):
        self.assertEqual(make_url('YHOO'), (
            'http://ichart.finance.yahoo.com/table.csv?'
            's=YHOO&d=&e=&f=&g=d&a=&b=&c=&ignore=.csv'
        ))

    def test_only_start_date(self):
        self.assertEqual(make_url('GOOG', start_date='20131122'), (
            'http://ichart.finance.yahoo.com/table.csv?'
            's=GOOG&d=&e=&f=&g=d&a=10&b=22&c=2013&ignore=.csv'
        ))

    def test_only_end_date(self):
        self.assertEqual(make_url('AAPL', end_date='20131122'), (
            'http://ichart.finance.yahoo.com/table.csv?'
            's=AAPL&d=10&e=22&f=2013&g=d&a=&b=&c=&ignore=.csv'
        ))

    def test_start_and_end_dates(self):
        self.assertEqual(make_url('TSLA', start_date='20120305', end_date='20131122'), (
            'http://ichart.finance.yahoo.com/table.csv?'
            's=TSLA&d=10&e=22&f=2013&g=d&a=2&b=5&c=2012&ignore=.csv'
        ))


class YahooSpiderTest(TestCaseBase):

    def test_empty_creation(self):
        spider = YahooSpider()
        self.assertEqual(spider.start_urls, [])

    # TODO: more tests
