import cStringIO
import os

from pystock_crawler import utils
from pystock_crawler.tests.base import SAMPLE_DATA_DIR, TestCaseBase


class UtilsTest(TestCaseBase):

    def test_check_date_arg(self):
        utils.check_date_arg('19830305')
        utils.check_date_arg('19851122')
        utils.check_date_arg('19980720')
        utils.check_date_arg('20140212')

        # OK to pass an empty argument
        utils.check_date_arg('')

        with self.assertRaises(ValueError):
            utils.check_date_arg('1234')

        with self.assertRaises(ValueError):
            utils.check_date_arg('2014111')

        with self.assertRaises(ValueError):
            utils.check_date_arg('20141301')

        with self.assertRaises(ValueError):
            utils.check_date_arg('20140132')

    def test_parse_limit_arg(self):
        self.assertEqual(utils.parse_limit_arg(''), (0, None))
        self.assertEqual(utils.parse_limit_arg('11,22'), (11, 22))

        with self.assertRaises(ValueError):
            utils.parse_limit_arg('11,22,33')

        with self.assertRaises(ValueError):
            utils.parse_limit_arg('abc')

    def test_load_symbols(self):
        try:
            filename = os.path.join(SAMPLE_DATA_DIR, 'test_symbols.txt')
            with open(filename, 'w') as f:
                f.write('AAPL Apple Inc.\nGOOG\tGoogle Inc.\n# Comment\nFB\nTWTR\nAMZN\nSPY\n\nYHOO\n# The end\n')

            symbols = list(utils.load_symbols(filename))
            self.assertEqual(symbols, ['AAPL', 'GOOG', 'FB', 'TWTR', 'AMZN', 'SPY', 'YHOO'])
        finally:
            os.remove(filename)

    def test_parse_csv(self):
        f = cStringIO.StringIO('name,age\nAvon,30\nOmar,29\nJoe,45\n')
        items = list(utils.parse_csv(f))
        self.assertEqual(items, [
            { 'name': 'Avon', 'age': '30' },
            { 'name': 'Omar', 'age': '29' },
            { 'name': 'Joe', 'age': '45' }
        ])
