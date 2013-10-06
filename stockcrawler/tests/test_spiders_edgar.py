import os
import tempfile
import unittest

from stockcrawler.spiders.edgar import EdgarSpider, URLGenerator


def make_url(symbol, start_date='', end_date=''):
    return 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=10-&dateb=%s&datea=%s&owner=exclude&count=300' \
           % (symbol, end_date, start_date)


class URLGeneratorTest(unittest.TestCase):

    def test_no_dates(self):
        urls = URLGenerator(('FB', 'GOOG'))
        self.assertEqual(list(urls), [
            make_url('FB'), make_url('GOOG')
        ])

    def test_with_start_date(self):
        urls = URLGenerator(('AAPL', 'AMZN', 'GLD'), start_date='20120215')
        self.assertEqual(list(urls), [
            make_url('AAPL', start_date='20120215'),
            make_url('AMZN', start_date='20120215'),
            make_url('GLD', start_date='20120215')
        ])

    def test_with_end_date(self):
        urls = URLGenerator(('TSLA', 'USO', 'MMM'), end_date='20110530')
        self.assertEqual(list(urls), [
            make_url('TSLA', end_date='20110530'),
            make_url('USO', end_date='20110530'),
            make_url('MMM', end_date='20110530')
        ])

    def test_with_start_and_end_dates(self):
        urls = URLGenerator(('DDD', 'AXP', 'KO'), start_date='20111230', end_date='20121230')
        self.assertEqual(list(urls), [
            make_url('DDD', '20111230', '20121230'),
            make_url('AXP', '20111230', '20121230'),
            make_url('KO', '20111230', '20121230')
        ])


class EdgarSpiderTest(unittest.TestCase):

    def test_empty_creation(self):
        spider = EdgarSpider()
        self.assertEqual(spider.start_urls, [])

    def test_symbol_file(self):
        # create a mock file of a list of symbols
        f = tempfile.NamedTemporaryFile('w', delete=False)
        f.write('# Comment\nGOOG\nADBE\nLNKD\n#comment\nJPM\n')
        f.close()

        spider = EdgarSpider(symbols=f.name)
        urls = list(spider.start_urls)

        self.assertEqual(urls, [
            make_url('GOOG'), make_url('ADBE'),
            make_url('LNKD'), make_url('JPM')
        ])

        os.remove(f.name)

    def test_invalid_dates(self):
        with self.assertRaises(ValueError):
            EdgarSpider(startdate='12345678')

        with self.assertRaises(ValueError):
            EdgarSpider(enddate='12345678')

    def test_symbol_file_and_dates(self):
        # create a mock file of a list of symbols
        f = tempfile.NamedTemporaryFile('w', delete=False)
        f.write('# Comment\nT\nCBS\nWMT\n')
        f.close()

        spider = EdgarSpider(symbols=f.name, startdate='20110101', enddate='20130630')
        urls = list(spider.start_urls)

        self.assertEqual(urls, [
            make_url('T', '20110101', '20130630'),
            make_url('CBS', '20110101', '20130630'),
            make_url('WMT', '20110101', '20130630')
        ])

        os.remove(f.name)
