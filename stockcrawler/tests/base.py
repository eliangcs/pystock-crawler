import unittest


class TestCaseBase(unittest.TestCase):
    '''
    Provides utility functions for test cases.

    '''
    def assert_none_or_almost_equal(self, value, expected_value):
        if expected_value is None:
            self.assertIsNone(value)
        else:
            self.assertAlmostEqual(value, expected_value)

    def assert_item(self, item, expected):
        self.assertEqual(item.get('symbol'), expected.get('symbol'))
        self.assertEqual(item.get('amend'), expected.get('amend'))
        self.assertEqual(item.get('doc_type'), expected.get('doc_type'))
        self.assertEqual(item.get('period_focus'), expected.get('period_focus'))
        self.assertEqual(item.get('end_date'), expected.get('end_date'))
        self.assert_none_or_almost_equal(item.get('revenues'), expected.get('revenues'))
        self.assert_none_or_almost_equal(item.get('net_income'), expected.get('net_income'))
        self.assert_none_or_almost_equal(item.get('eps_basic'), expected.get('eps_basic'))
        self.assert_none_or_almost_equal(item.get('eps_diluted'), expected.get('eps_diluted'))
        self.assertAlmostEqual(item.get('dividend'), expected.get('dividend'))
        self.assert_none_or_almost_equal(item.get('assets'), expected.get('assets'))
        self.assert_none_or_almost_equal(item.get('equity'), expected.get('equity'))
        self.assert_none_or_almost_equal(item.get('cash'), expected.get('cash'))
