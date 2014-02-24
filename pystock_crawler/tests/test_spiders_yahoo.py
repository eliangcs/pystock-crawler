import os
import tempfile

from scrapy.http import TextResponse

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
        self.assertEqual(list(spider.start_urls), [])

    def test_inline_symbols(self):
        spider = YahooSpider(symbols='C')
        self.assertEqual(list(spider.start_urls), [make_url('C')])

        spider = YahooSpider(symbols='KO,DIS,ATVI')
        self.assertEqual(list(spider.start_urls), [
            make_url(symbol) for symbol in ('KO', 'DIS', 'ATVI')
        ])

    def test_symbol_file(self):
        try:
            # Create a mock file of a list of symbols
            with tempfile.NamedTemporaryFile('w', delete=False) as f:
                f.write('# Comment\nGOOG\tGoogle Inc.\nAAPL\nFB  Facebook.com\n#comment\nAMZN\n')

            spider = YahooSpider(symbols=f.name)
            self.assertEqual(list(spider.start_urls), [
                make_url(symbol) for symbol in ('GOOG', 'AAPL', 'FB', 'AMZN')
            ])
        finally:
            os.remove(f.name)

    def test_illegal_dates(self):
        with self.assertRaises(ValueError):
            YahooSpider(startdate='12345678')

        with self.assertRaises(ValueError):
            YahooSpider(enddate='12345678')

    def test_parse(self):
        spider = YahooSpider()

        body = ('Date,Open,High,Low,Close,Volume,Adj Close\n'
                '2013-11-22,121.58,122.75,117.93,121.38,11096700,121.38\n'
                '2013-09-06,168.57,169.70,165.15,166.97,8619700,166.97\n'
                '2013-06-26,103.80,105.87,102.66,105.72,6602600,105.72\n')
        response = TextResponse(make_url('YHOO'), body=body)
        items = list(spider.parse(response))

        self.assertEqual(len(items), 3)
        self.assert_item(items[0], {
            'symbol': 'YHOO',
            'date': '2013-11-22',
            'open': 121.58,
            'high': 122.75,
            'low': 117.93,
            'close': 121.38,
            'volume': 11096700,
            'adj_close': 121.38
        })
        self.assert_item(items[1], {
            'symbol': 'YHOO',
            'date': '2013-09-06',
            'open': 168.57,
            'high': 169.70,
            'low': 165.15,
            'close': 166.97,
            'volume': 8619700,
            'adj_close': 166.97
        })
        self.assert_item(items[2], {
            'symbol': 'YHOO',
            'date': '2013-06-26',
            'open': 103.80,
            'high': 105.87,
            'low': 102.66,
            'close': 105.72,
            'volume': 6602600,
            'adj_close': 105.72
        })
