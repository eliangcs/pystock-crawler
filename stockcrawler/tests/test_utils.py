from stockcrawler import utils
from stockcrawler.tests.base import TestCaseBase


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
