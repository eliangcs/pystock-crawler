import os
import unittest

from scrapy.http.response.xml import XmlResponse

from stockcrawler.loaders import ReportLoader


def create_response(filename):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data', filename)
    with open(path) as f:
        body = f.read()
    return XmlResponse('file://%s' % path.replace('\\', '/'), body=body)


def parse_xml(filename):
    response = create_response(filename)
    loader = ReportLoader(response=response)
    return loader.load_item()


class TestReportLoader(unittest.TestCase):

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

    def test_goog_20130630(self):
        item = parse_xml('goog-20130630.xml')
        self.assert_item(item, {
            'symbol': 'GOOG',
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2013-06-30',
            'revenues': 14105000000.0,
            'net_income': 3228000000.0,
            'num_shares': 332480000,
            'eps_basic': 9.71,
            'eps_diluted': 9.54,
            'dividend': 0.0,
            'assets': 101182000000.0,
            'equity': 78852000000.0,
            'cash': 16164000000.0
        })

    def test_msft_20110630(self):
        item = parse_xml('msft-20110630.xml')
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

    def test_ko_20120928(self):
        item = parse_xml('ko-20120928.xml')
        self.assert_item(item, {
            'symbol': 'KO',
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2012-09-28',
            'revenues': 12340000000.0,
            'net_income': 2311000000.0,
            'num_shares': 4502000000,
            'eps_basic': 0.51,
            'eps_diluted': 0.50,
            'dividend': 0.255,
            'assets': 86654000000.0,
            'equity': 33590000000.0,
            'cash': 9615000000.0
        })
