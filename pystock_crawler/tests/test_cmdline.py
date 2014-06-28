import os
import shutil
import subprocess
import unittest

import pystock_crawler

from envoy import run, expand_args


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


class CrawlSymbolsTest(unittest.TestCase):

    def setUp(self):
        if os.path.isdir(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        os.mkdir(TEST_DIR)

        self.args = {
            'output': os.path.join(TEST_DIR, 'symbols.txt'),
            'log_file': os.path.join(TEST_DIR, 'symbols.log'),
            'working_dir': TEST_DIR
        }

    def assert_cache(self):
        # Check if cache is there
        cache_dir = os.path.join(TEST_DIR, '.scrapy', 'httpcache', 'nasdaq.leveldb')
        self.assertTrue(os.path.isdir(cache_dir))

    def get_output_content(self):
        output_path = self.args['output']

        os.system('touch %s' % os.path.join(TEST_DIR, 'hello'))
        cmd = 'scrapy crawl nasdaq -a exchanges="NYSE" -t symbollist -o "/home/travis/build/eliangcs/pystock-crawler/test_data/envoy.txt" -s LOG_FILE="/home/travis/build/eliangcs/pystock-crawler/test_data/envoy.log"'
        run(cmd)
        process = subprocess.Popen([
            'scrapy', 'crawl', 'nasdaq',
            '-a', 'exchanges="NYSE"',
            '-t', 'symbollist',
            '-o', '/home/travis/build/eliangcs/pystock-crawler/test_data/popen.txt',
            '-s', 'LOG_FILE="/home/travis/build/eliangcs/pystock-crawler/test_data/popen.log"'
        ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
        process.communicate()

        print '### Envoy'
        with open('./test_data/envoy.txt') as f:
            print f.read()[0:200]

        print '### Popen'
        with open('./test_data/popen.txt') as f:
            print f.read()[0:200]

        print '### expand_args'
        print expand_args(cmd)

        with open(self.args['log_file']) as f:
            print f.read()

        print os.getcwd()
        print os.listdir(os.getcwd())
        print output_path
        print os.listdir(TEST_DIR)

        self.assertTrue(os.path.isfile(output_path))

        with open(output_path) as f:
            content = f.read()
        return content

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

    def assert_log(self):
        # Check if log file is there
        log_path = self.args['log_file']
        self.assertTrue(os.path.isfile(log_path))

    def tearDown(self):
        shutil.rmtree(TEST_DIR)

    def test_crawl_nyse(self):
        r = run('./bin/pystock-crawler symbols NYSE -o %(output)s -l %(log_file)s -w %(working_dir)s' % self.args)
        self.assertEqual(r.status_code, 0)
        print r.std_out
        print r.std_err
        self.assert_nyse_output()
        self.assert_log()
        self.assert_cache()

    def test_crawl_nyse_and_nasdaq(self):
        r = run('./bin/pystock-crawler symbols NYSE,NASDAQ -o %(output)s -l %(log_file)s -w %(working_dir)s' % self.args)
        self.assertEqual(r.status_code, 0)
        print r.std_out
        print r.std_err
        self.assert_nyse_and_nasdaq_output()
        self.assert_log()
        self.assert_cache()
