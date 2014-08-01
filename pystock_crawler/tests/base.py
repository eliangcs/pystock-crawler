import os
import unittest


# Stores temporary test data
SAMPLE_DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data')


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
        self.assertEqual(item.get('name'), expected.get('name'))
        self.assertEqual(item.get('amend'), expected.get('amend'))
        self.assertEqual(item.get('doc_type'), expected.get('doc_type'))
        self.assertEqual(item.get('period_focus'), expected.get('period_focus'))
        self.assertEqual(item.get('fiscal_year'), expected.get('fiscal_year'))
        self.assertEqual(item.get('end_date'), expected.get('end_date'))
        self.assert_none_or_almost_equal(item.get('revenues'), expected.get('revenues'))
        self.assert_none_or_almost_equal(item.get('net_income'), expected.get('net_income'))
        self.assert_none_or_almost_equal(item.get('eps_basic'), expected.get('eps_basic'))
        self.assert_none_or_almost_equal(item.get('eps_diluted'), expected.get('eps_diluted'))
        self.assertAlmostEqual(item.get('dividend'), expected.get('dividend'))
        self.assert_none_or_almost_equal(item.get('assets'), expected.get('assets'))
        self.assert_none_or_almost_equal(item.get('equity'), expected.get('equity'))
        self.assert_none_or_almost_equal(item.get('cash'), expected.get('cash'))
        self.assert_none_or_almost_equal(item.get('op_income'), expected.get('op_income'))
        self.assert_none_or_almost_equal(item.get('cur_assets'), expected.get('cur_assets'))
        self.assert_none_or_almost_equal(item.get('cur_liab'), expected.get('cur_liab'))
        self.assert_none_or_almost_equal(item.get('cash_flow_op'), expected.get('cash_flow_op'))
        self.assert_none_or_almost_equal(item.get('cash_flow_inv'), expected.get('cash_flow_inv'))
        self.assert_none_or_almost_equal(item.get('cash_flow_fin'), expected.get('cash_flow_fin'))


def _create_sample_data_dir():
    if not os.path.exists(SAMPLE_DATA_DIR):
        try:
            os.makedirs(SAMPLE_DATA_DIR)
        except OSError:
            pass

    assert os.path.exists(SAMPLE_DATA_DIR)

_create_sample_data_dir()
