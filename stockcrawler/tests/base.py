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
        self.assertEqual(item['symbol'], expected['symbol'])
        self.assertEqual(item['amend'], expected['amend'])
        self.assertEqual(item['doc_type'], expected['doc_type'])
        self.assertEqual(item['period_focus'], expected['period_focus'])
        self.assertEqual(item['end_date'], expected['end_date'])
        self.assert_none_or_almost_equal(item['revenues'], expected['revenues'])
        self.assert_none_or_almost_equal(item['net_income'], expected['net_income'])
        self.assert_none_or_almost_equal(item['eps_basic'], expected['eps_basic'])
        self.assert_none_or_almost_equal(item['eps_diluted'], expected['eps_diluted'])
        self.assertAlmostEqual(item['dividend'], expected['dividend'])
        self.assert_none_or_almost_equal(item['assets'], expected['assets'])
        self.assert_none_or_almost_equal(item['equity'], expected['equity'])
        self.assert_none_or_almost_equal(item['cash'], expected['cash'])
