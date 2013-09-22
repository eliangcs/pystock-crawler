import os
import unittest

from scrapy.http.response.xml import XmlResponse

from stockcrawler.loaders import ReportLoader


def create_response(filename):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data', filename)
    with open(path) as f:
        body = f.read()
    return XmlResponse('file://%s' % path, body=body)


class TestReportLoader(unittest.TestCase):

    def setUp(self):
        self.abc = 1

    def parse_xml(self, filename):
        response = create_response('msft-20110630.xml')
        loader = ReportLoader(response=response)
        return loader.load_item()

    def assert_item(self, item, expected):
        self.assertEqual(item['symbol'], expected['symbol'])
        self.assertEqual(item['doc_type'], expected['doc_type'])
        self.assertEqual(item['period_focus'], expected['period_focus'])
        self.assertEqual(item['end_date'], expected['end_date'])
        self.assertEqual(item['revenues'], expected['revenues'])
        self.assertEqual(item['net_income'], expected['net_income'])
        self.assertEqual(item['num_shares'], expected['num_shares'])
        self.assertEqual(item['eps_basic'], expected['eps_basic'])
        self.assertEqual(item['eps_diluted'], expected['eps_diluted'])
        self.assertEqual(item['dividend'], expected['dividend'])
        self.assertEqual(item['assets'], expected['assets'])
        self.assertEqual(item['equity'], expected['equity'])
        self.assertEqual(item['cash'], expected['cash'])

    def test_msft_20110630(self):
        item = self.parse_xml('msft-20110630.xml')
        self.assert_item(item, {
            'symbol': 'MSFT',
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2011-06-30',
            'revenues': 69943000000.0,
            'net_income': 23150000000.0,
            'num_shares': 8490000000,
            'eps_basic': 2.73,
            'eps_diluted': 2.69,
            'dividend': 0.64,
            'assets': 108704000000.0,
            'equity': 57083000000.0,
            'cash': 9610000000.0
        })
