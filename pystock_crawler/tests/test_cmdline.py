import os
import shutil
import unittest

import pystock_crawler

from envoy import run


TEST_DIR = './test_data'


class PrintTest(unittest.TestCase):

    def test_no_args(self):
        r = run('./bin/pystock-crawler')
        self.assertIn('Usage:', r.std_err)

    def test_print_help(self):
        r = run('./bin/pystock-crawler -h')
        self.assertIn('Usage:', r.std_out)

        r2 = run('./bin/pystock-crawler --help')
        self.assertEqual(r.std_out, r2.std_out)

    def test_print_version(self):
        r = run('./bin/pystock-crawler -v')
        self.assertEqual(r.std_out, 'pystock-crawler %s\n' % pystock_crawler.__version__)

        r2 = run('./bin/pystock-crawler --version')
        self.assertEqual(r.std_out, r2.std_out)


class CrawlTest(unittest.TestCase):
    '''Base class for crawl test cases.'''
    def setUp(self):
        if os.path.isdir(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        os.mkdir(TEST_DIR)

        self.args = {
            'output': os.path.join(TEST_DIR, '%s.out' % self.filename),
            'log_file': os.path.join(TEST_DIR, '%s.log' % self.filename),
            'working_dir': TEST_DIR
        }

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def assert_cache(self):
        # Check if cache is there
        cache_dir = os.path.join(TEST_DIR, '.scrapy', 'httpcache', '%s.leveldb' % self.spider)
        self.assertTrue(os.path.isdir(cache_dir))

    def assert_log(self):
        # Check if log file is there
        log_path = self.args['log_file']
        self.assertTrue(os.path.isfile(log_path))

    def get_output_content(self):
        output_path = self.args['output']
        self.assertTrue(os.path.isfile(output_path))

        with open(output_path) as f:
            content = f.read()
        return content


class CrawlSymbolsTest(CrawlTest):

    filename = 'symbols'
    spider = 'nasdaq'

    def assert_nyse_output(self):
        # Check if some common NYSE symbols are in output
        content = self.get_output_content()
        self.assertIn('JPM', content)
        self.assertIn('KO', content)
        self.assertIn('WMT', content)

        # NASDAQ symbols shouldn't be
        self.assertNotIn('AAPL', content)
        self.assertNotIn('GOOG', content)
        self.assertNotIn('YHOO', content)

    def assert_nyse_and_nasdaq_output(self):
        # Check if some common NYSE symbols are in output
        content = self.get_output_content()
        self.assertIn('JPM', content)
        self.assertIn('KO', content)
        self.assertIn('WMT', content)

        # Check if some common NASDAQ symbols are in output
        self.assertIn('AAPL', content)
        self.assertIn('GOOG', content)
        self.assertIn('YHOO', content)

    def test_crawl_nyse(self):
        r = run('./bin/pystock-crawler symbols NYSE -o %(output)s -l %(log_file)s -w %(working_dir)s' % self.args)
        self.assertEqual(r.status_code, 0)
        self.assert_nyse_output()
        self.assert_log()
        self.assert_cache()

    def test_crawl_nyse_and_nasdaq(self):
        r = run('./bin/pystock-crawler symbols NYSE,NASDAQ -o %(output)s -l %(log_file)s -w %(working_dir)s --sort' % self.args)
        self.assertEqual(r.status_code, 0)
        self.assert_nyse_and_nasdaq_output()
        self.assert_log()
        self.assert_cache()


class CrawlPricesTest(CrawlTest):

    filename = 'prices'
    spider = 'yahoo'

    def test_crawl_inline_symbols(self):
        r = run('./bin/pystock-crawler prices GOOG,IBM -o %(output)s -l %(log_file)s -w %(working_dir)s' % self.args)
        self.assertEqual(r.status_code, 0)

        content = self.get_output_content()
        self.assertIn('GOOG', content)
        self.assertIn('IBM', content)
        self.assert_log()
        self.assert_cache()

    def test_crawl_symbol_file(self):
        # Create a sample symbol file
        symbol_file = os.path.join(TEST_DIR, 'symbols.txt')
        with open(symbol_file, 'w') as f:
            f.write('WMT\nJPM')
        self.args['symbol_file'] = symbol_file

        r = run('./bin/pystock-crawler prices %(symbol_file)s -o %(output)s -l %(log_file)s -w %(working_dir)s --sort' % self.args)
        self.assertEqual(r.status_code, 0)

        content = self.get_output_content()
        self.assertIn('WMT', content)
        self.assertIn('JPM', content)
        self.assert_log()
        self.assert_cache()


class CrawlReportsTest(CrawlTest):

    filename = 'reports'
    spider = 'edgar'

    def test_crawl_inline_symbols(self):
        r = run('./bin/pystock-crawler reports KO,MCD -o %(output)s -l %(log_file)s -w %(working_dir)s '
                '-s 20130401 -e 20130531' % self.args)
        self.assertEqual(r.status_code, 0)

        content = self.get_output_content()
        self.assertIn('KO', content)
        self.assertIn('MCD', content)
        self.assert_log()
        self.assert_cache()

    def test_crawl_symbol_file(self):
        # Create a sample symbol file
        symbol_file = os.path.join(TEST_DIR, 'symbols.txt')
        with open(symbol_file, 'w') as f:
            f.write('KO\nMCD')
        self.args['symbol_file'] = symbol_file

        r = run('./bin/pystock-crawler reports %(symbol_file)s -o %(output)s -l %(log_file)s -w %(working_dir)s '
                '-s 20130401 -e 20130531 --sort' % self.args)
        self.assertEqual(r.status_code, 0)

        content = self.get_output_content()
        self.assertIn('KO', content)
        self.assertIn('MCD', content)
        self.assert_log()
        self.assert_cache()
