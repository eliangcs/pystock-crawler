import os

from stockcrawler import utils
from stockcrawler.tests.base import SAMPLE_DATA_DIR, TestCaseBase


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

    def test_load_symbols(self):
        try:
            filename = os.path.join(SAMPLE_DATA_DIR, 'test_symbols.txt')
            with open(filename, 'w') as f:
                f.write('AAPL\nGOOG\n# Comment\nFB\nTWTR\nAMZN\nSPY\n\nYHOO\n# The end\n')

            symbols = list(utils.load_symbols(filename))
            self.assertEqual(symbols, ['AAPL', 'GOOG', 'FB', 'TWTR', 'AMZN', 'SPY', 'YHOO'])
        finally:
            try:
                os.remove(filename)
            except OSError:
                pass
