import os
import requests
import unittest

from scrapy.http.response.xml import XmlResponse

from stockcrawler.loaders import ReportItemLoader


def create_response(file_path):
    with open(file_path) as f:
        body = f.read()
    return XmlResponse('file://%s' % file_path.replace('\\', '/'), body=body)


def download(url, local_path):
    if not os.path.exists(local_path):
        dir_path = os.path.dirname(local_path)
        if not os.path.exists(dir_path):
            try:
                os.mkdir(dir_path)
            except OSError:
                pass

        with open(local_path, 'wb') as f:
            r = requests.get(url, stream=True)
            for chunk in r.iter_content(chunk_size=4096):
                f.write(chunk)


def parse_xml(url):
    filename = url.split('/')[-1]
    local_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data', filename)
    download(url, local_path)
    response = create_response(local_path)
    loader = ReportItemLoader(response=response)
    return loader.load_item()


class ReportItemLoaderTest(unittest.TestCase):

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

    def test_aapl_20100626(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/320193/000119312510162840/aapl-20100626.xml')
        self.assert_item(item, {
            'symbol': 'AAPL',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2010-06-26',
            'revenues': 15700000000.0,
            'net_income': 3253000000.0,
            'eps_basic': 3.57,
            'eps_diluted': 3.51,
            'dividend': 0.0,
            'assets': 64725000000.0,
            'equity': 43111000000.0,
            'cash': 9705000000.0
        })

    def test_aapl_20110326(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/320193/000119312511104388/aapl-20110326.xml')
        self.assert_item(item, {
            'symbol': 'AAPL',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2011-03-26',
            'revenues': 24667000000.0,
            'net_income': 5987000000.0,
            'eps_basic': 6.49,
            'eps_diluted': 6.40,
            'dividend': 0.0,
            'assets': 94904000000.0,
            'equity': 61477000000.0,
            'cash': 15978000000.0
        })

    def test_aapl_20120929(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/320193/000119312512444068/aapl-20120929.xml')
        self.assert_item(item, {
            'symbol': 'AAPL',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2012-09-29',
            'revenues': 156508000000.0,
            'net_income': 41733000000.0,
            'eps_basic': 44.64,
            'eps_diluted': 44.15,
            'dividend': 2.65,
            'assets': 176064000000.0,
            'equity': 118210000000.0,
            'cash': 10746000000.0
        })

    def test_adbe_20090227(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/796343/000079634309000021/adbe-20090227.xml')
        self.assert_item(item, {
            'symbol': 'ADBE',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2009-02-27',
            'revenues': 786390000.0,
            'net_income': 156435000.0,
            'eps_basic': 0.3,
            'eps_diluted': 0.3,
            'dividend': 0.0,
            'assets': 5887596000.0,
            'equity': 4611160000.0,
            'cash': 1148925000.0
        })

    def test_axp_20100930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/4962/000095012310100214/axp-20100930.xml')
        self.assert_item(item, {
            'symbol': 'AXP',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2010-09-30',
            'revenues': 6660000000.0,
            'net_income': 1093000000.0,
            'eps_basic': 0.91,
            'eps_diluted': 0.9,
            'dividend': 0.18,
            'assets': 146056000000.0,
            'equity': 15920000000.0,
            'cash': 21341000000.0
        })

    def test_axp_20120630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/4962/000119312512332179/axp-20120630.xml')
        self.assert_item(item, {
            'symbol': 'AXP',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2012-06-30',
            'revenues': 7504000000.0,
            'net_income': 1339000000.0,
            'eps_basic': 1.16,
            'eps_diluted': 1.15,
            'dividend': 0.2,
            'assets': 148128000000.0,
            'equity': 19267000000.0,
            'cash': 22072000000.0
        })

    def test_axp_20121231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/4962/000119312513070554/axp-20121231.xml')
        self.assert_item(item, {
            'symbol': 'AXP',
            'amend': True,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2012-12-31',
            'revenues': 29592000000.0,
            'net_income': 4482000000.0,
            'eps_basic': 3.91,
            'eps_diluted': 3.89,
            'dividend': 0.8,
            'assets': 153140000000.0,
            'equity': 18886000000.0,
            'cash': 22250000000.0
        })

    def test_ba_20091231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12927/000119312510024406/ba-20091231.xml')
        self.assert_item(item, {
            'symbol': 'BA',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2009-12-31',
            'revenues': 68281000000.0,
            'net_income': 1312000000.0,
            'eps_basic': 1.86,
            'eps_diluted': 1.84,
            'dividend': 1.68,
            'assets': 62053000000.0,
            'equity': 2225000000.0,
            'cash': 9215000000.0
        })

    def test_ba_20110930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12927/000119312511281613/ba-20110930.xml')
        self.assert_item(item, {
            'symbol': 'BA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2011-09-30',
            'revenues': 17727000000.0,
            'net_income': 1098000000.0,
            'eps_basic': 1.47,
            'eps_diluted': 1.46,
            'dividend': 0.42,
            'assets': 74163000000.0,
            'equity': 6061000000.0,
            'cash': 5954000000.0
        })

    def test_ba_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12927/000001292713000023/ba-20130331.xml')
        self.assert_item(item, {
            'symbol': 'BA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2013-03-31',
            'revenues': 18893000000.0,
            'net_income': 1106000000.0,
            'eps_basic': 1.45,
            'eps_diluted': 1.44,
            'dividend': 0.49,
            'assets': 90447000000.0,
            'equity': 7560000000.0,
            'cash': 8335000000.0
        })

    def test_cbs_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/813828/000104746910004823/cbs-20100331.xml')
        self.assert_item(item, {
            'symbol': 'CBS',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2010-03-31',
            'revenues': 3530900000.0,
            'net_income': -26200000.0,
            'eps_basic': -0.04,
            'eps_diluted': -0.04,
            'dividend': 0.05,
            'assets': 26756100000.0,
            'equity': 9046100000.0,
            'cash': 872700000.0
        })

    def test_cbs_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/813828/000104746912001373/cbs-20111231.xml')
        self.assert_item(item, {
            'symbol': 'CBS',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2011-12-31',
            'revenues': 14245000000.0,
            'net_income': 1305000000.0,
            'eps_basic': 1.97,
            'eps_diluted': 1.92,
            'dividend': 0.35,
            'assets': 26197000000.0,
            'equity': 9908000000.0,
            'cash': 660000000.0
        })

    def test_cbs_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/813828/000104746913007929/cbs-20130630.xml')
        self.assert_item(item, {
            'symbol': 'CBS',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2013-06-30',
            'revenues': 3699000000.0,
            'net_income': 472000000.0,
            'eps_basic': 0.78,
            'eps_diluted': 0.76,
            'dividend': 0.12,
            'assets': 25693000000.0,
            'equity': 9601000000.0,
            'cash': 282000000.0
        })

    def test_ccmm_20110630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1091667/000109166711000103/ccmm-20110630.xml')
        self.assert_item(item, {
            'symbol': 'CCMM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2011-06-30',
            'revenues': 1791000000.0,
            'net_income': -107000000.0,
            'eps_basic': -0.98,
            'eps_diluted': -0.98,
            'dividend': 0.0,
            'assets': None,
            'equity': None,
            'cash': None
        })

    def test_dltr_20130504(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/935703/000093570313000029/dltr-20130504.xml')
        self.assert_item(item, {
            'symbol': 'DLTR',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2013-05-04',
            'revenues': 1865800000.0,
            'net_income': 133500000.0,
            'eps_basic': 0.6,
            'eps_diluted': 0.59,
            'dividend': 0.0,
            'assets': 2811800000.0,
            'equity': 1739700000.0,
            'cash': 383300000.0
        })

    def test_ebay_20100630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1065088/000119312510164115/ebay-20100630.xml')
        self.assert_item(item, {
            'symbol': 'EBAY',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2010-06-30',
            'revenues': 2215379000.0,
            'net_income': 412192000.0,
            'eps_basic': 0.31,
            'eps_diluted': 0.31,
            'dividend': 0.0,
            'assets': 18747584000.0,
            'equity': 14169291000.0,
            'cash': 4037442000.0
        })

    def test_fb_20120630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1326801/000119312512325997/fb-20120630.xml')
        self.assert_item(item, {
            'symbol': 'FB',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2012-06-30',
            'revenues': 1184000000.0,
            'net_income': -157000000.0,
            'eps_basic': -0.08,
            'eps_diluted': -0.08,
            'dividend': 0.0,
            'assets': 14928000000.0,
            'equity': 13309000000.0,
            'cash': 2098000000.0
        })

    def test_fb_20121231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1326801/000132680113000003/fb-20121231.xml')
        self.assert_item(item, {
            'symbol': 'FB',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2012-12-31',
            'revenues': 5089000000.0,
            'net_income': 32000000.0,
            'eps_basic': 0.02,
            'eps_diluted': 0.01,
            'dividend': 0.0,
            'assets': 15103000000.0,
            'equity': 11755000000.0,
            'cash': 2384000000.0
        })

    def test_goog_20090930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1288776/000119312509222384/goog-20090930.xml')
        self.assert_item(item, {
            'symbol': 'GOOG',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2009-09-30',
            'revenues': 5944851000.0,
            'net_income': 1638975000.0,
            'eps_basic': 5.18,
            'eps_diluted': 5.13,
            'dividend': 0.0,
            'assets': 37702845000.0,
            'equity': 33721753000.0,
            'cash': 12087115000.0
        })

    def test_goog_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1288776/000119312512440217/goog-20120930.xml')
        self.assert_item(item, {
            'symbol': 'GOOG',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2012-09-30',
            'revenues': 14101000000.0,
            'net_income': 2176000000.0,
            'eps_basic': 6.64,
            'eps_diluted': 6.53,
            'dividend': 0.0,
            'assets': 89730000000.0,
            'equity': 68028000000.0,
            'cash': 16260000000.0
        })

    def test_goog_20121231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1288776/000119312513028362/goog-20121231.xml')
        self.assert_item(item, {
            'symbol': 'GOOG',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2012-12-31',
            'revenues': 50175000000.0,
            'net_income': 10737000000.0,
            'eps_basic': 32.81,
            'eps_diluted': 32.31,
            'dividend': 0.0,
            'assets': 93798000000.0,
            'equity': 71715000000.0,
            'cash': 14778000000.0
        })

    def test_goog_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1288776/000128877613000055/goog-20130630.xml')
        self.assert_item(item, {
            'symbol': 'GOOG',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2013-06-30',
            'revenues': 14105000000.0,
            'net_income': 3228000000.0,
            'eps_basic': 9.71,
            'eps_diluted': 9.54,
            'dividend': 0.0,
            'assets': 101182000000.0,
            'equity': 78852000000.0,
            'cash': 16164000000.0
        })

    def test_jnj_20120101(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/200406/000119312512075565/jnj-20120101.xml')
        self.assert_item(item, {
            'symbol': 'JNJ',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2012-01-01',
            'revenues': 65030000000.0,
            'net_income': 9672000000.0,
            'eps_basic': 3.54,
            'eps_diluted': 3.49,
            'dividend': 2.25,
            'assets': 113644000000.0,
            'equity': 57080000000.0,
            'cash': 24542000000.0
        })

    def test_jnj_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/200406/000020040612000140/jnj-20120930.xml')
        self.assert_item(item, {
            'symbol': 'JNJ',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2012-09-30',
            'revenues': 17052000000.0,
            'net_income': 2968000000.0,
            'eps_basic': 1.08,
            'eps_diluted': 1.05,
            'dividend': 0.61,
            'assets': 118951000000.0,
            'equity': 63761000000.0,
            'cash': 15486000000.0
        })

    def test_jnj_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/200406/000020040613000091/jnj-20130630.xml')
        self.assert_item(item, {
            'symbol': 'JNJ',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2013-06-30',
            'revenues': 17877000000.0,
            'net_income': 3833000000.0,
            'eps_basic': 1.36,
            'eps_diluted': 1.33,
            'dividend': 0.66,
            'assets': 124325000000.0,
            'equity': 69665000000.0,
            'cash': 17307000000.0
        })

    def test_jpm_20090630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/19617/000095012309032832/jpm-20090630.xml')
        self.assert_item(item, {
            'symbol': 'JPM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2009-06-30',
            'revenues': 25623000000.0,
            'net_income': 1072000000.0,
            'eps_basic': 0.28,
            'eps_diluted': 0.28,
            'dividend': 0.05,
            'assets': 2026642000000.0,
            'equity': 154766000000.0,
            'cash': 25133000000.0
        })

    def test_jpm_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/19617/000001961712000163/jpm-20111231.xml')
        self.assert_item(item, {
            'symbol': 'JPM',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2011-12-31',
            'revenues': 97234000000.0,
            'net_income': 17568000000.0,
            'eps_basic': 4.50,
            'eps_diluted': 4.48,
            'dividend': 1.0,
            'assets': 2265792000000.0,
            'equity': 183573000000.0,
            'cash': 59602000000.0
        })

    def test_jpm_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/19617/000001961713000300/jpm-20130331.xml')
        self.assert_item(item, {
            'symbol': 'JPM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2013-03-31',
            'revenues': 25122000000.0,
            'net_income': 6131000000.0,
            'eps_basic': 1.61,
            'eps_diluted': 1.59,
            'dividend': 0.30,
            'assets': 2389349000000.0,
            'equity': 207086000000.0,
            'cash': 45524000000.0
        })

    def test_ko_20100402(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/21344/000104746910004416/ko-20100402.xml')
        self.assert_item(item, {
            'symbol': 'KO',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2010-04-02',
            'revenues': 7525000000.0,
            'net_income': 1614000000.0,
            'eps_basic': 0.70,
            'eps_diluted': 0.69,
            'dividend': 0.44,
            'assets': 47403000000.0,
            'equity': 25157000000.0,
            'cash': 5684000000.0
        })

    def test_ko_20101231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/21344/000104746911001506/ko-20101231.xml')
        self.assert_item(item, {
            'symbol': 'KO',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2010-12-31',
            'revenues': 35119000000.0,
            'net_income': 11809000000.0,
            'eps_basic': 5.12,
            'eps_diluted': 5.06,
            'dividend': 1.76,
            'assets': 72921000000.0,
            'equity': 31317000000.0,
            'cash': 8517000000.0
        })

    def test_ko_20120928(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/21344/000002134412000051/ko-20120928.xml')
        self.assert_item(item, {
            'symbol': 'KO',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2012-09-28',
            'revenues': 12340000000.0,
            'net_income': 2311000000.0,
            'eps_basic': 0.51,
            'eps_diluted': 0.50,
            'dividend': 0.255,
            'assets': 86654000000.0,
            'equity': 33590000000.0,
            'cash': 9615000000.0
        })

    def test_lcapa_20110930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1507934/000150793411000006/lcapa-20110930.xml')
        self.assert_item(item, {
            'symbol': 'LCAPA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2011-09-30',
            'revenues': 540000000.0,
            'net_income': -42000000.0,
            'eps_basic': -0.07,
            'eps_diluted': -0.12,
            'dividend': 0.0,
            'assets': 8915000000.0,
            'equity': 5078000000.0,
            'cash': 1937000000.0
        })

    def test_linta_20120331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1355096/000135509612000008/linta-20120331.xml')
        self.assert_item(item, {
            'symbol': 'LINTA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2012-03-31',
            'revenues': 2314000000.0,
            'net_income': 91000000.0,
            'eps_basic': 0.16,
            'eps_diluted': 0.16,
            'dividend': 0.0,
            'assets': 17144000000.0,
            'equity': 6505000000.0,
            'cash': 794000000.0
        })

    def test_lltc_20110102(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/791907/000079190711000016/lltc-20110102.xml')
        self.assert_item(item, {
            'symbol': 'LLTC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2011-01-02',
            'revenues': 383621000.0,
            'net_income': 143743000.0,
            'eps_basic': 0.62,
            'eps_diluted': 0.62,
            'dividend': 0.23,
            'assets': 1446186000.0,
            'equity': 278793000.0,
            'cash': 203308000.0
        })

    def test_lmca_20120331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1507934/000150793412000012/lmca-20120331.xml')
        self.assert_item(item, {
            'symbol': 'LMCA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2012-03-31',
            'revenues': 440000000.0,
            'net_income': 137000000.0,
            'eps_basic': 1.13,
            'eps_diluted': 1.10,
            'dividend': 0.0,
            'assets': 7122000000.0,
            'equity': 5321000000.0,
            'cash': 1915000000.0
        })

    def test_mmm_20091231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/66740/000110465910007295/mmm-20091231.xml')
        self.assert_item(item, {
            'symbol': 'MMM',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2009-12-31',
            'revenues': 23123000000.0,
            'net_income': 3193000000.0,
            'eps_basic': 4.56,
            'eps_diluted': 4.52,
            'dividend': 2.04,
            'assets': 27250000000.0,
            'equity': 13302000000.0,
            'cash': 3040000000.0
        })

    def test_mmm_20120331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/66740/000110465912032441/mmm-20120331.xml')
        self.assert_item(item, {
            'symbol': 'MMM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2012-03-31',
            'revenues': 7486000000.0,
            'net_income': 1125000000.0,
            'eps_basic': 1.61,
            'eps_diluted': 1.59,
            'dividend': 0.59,
            'assets': 32015000000.0,
            'equity': 16619000000.0,
            'cash': 2332000000.0
        })

    def test_mmm_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/66740/000110465913058961/mmm-20130630.xml')
        self.assert_item(item, {
            'symbol': 'MMM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2013-06-30',
            'revenues': 7752000000.0,
            'net_income': 1197000000.0,
            'eps_basic': 1.74,
            'eps_diluted': 1.71,
            'dividend': 0.635,
            'assets': 34130000000.0,
            'equity': 18319000000.0,
            'cash': 2942000000.0
        })

    def test_mnst_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/865752/000110465913062263/mnst-20130630.xml')
        self.assert_item(item, {
            'symbol': 'MNST',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2013-06-30',
            'revenues': 630934000.0,
            'net_income': 106873000.0,
            'eps_basic': 0.64,
            'eps_diluted': 0.62,
            'dividend': 0.0,
            'assets': 1317842000.0,
            'equity': 856021000.0,
            'cash': 283839000.0
        })

    def test_msft_20110630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/789019/000119312511200680/msft-20110630.xml')
        self.assert_item(item, {
            'symbol': 'MSFT',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2011-06-30',
            'revenues': 69943000000.0,
            'net_income': 23150000000.0,
            'eps_basic': 2.73,
            'eps_diluted': 2.69,
            'dividend': 0.64,
            'assets': 108704000000.0,
            'equity': 57083000000.0,
            'cash': 9610000000.0
        })

    def test_msft_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/789019/000119312512026864/msft-20111231.xml')
        self.assert_item(item, {
            'symbol': 'MSFT',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2011-12-31',
            'revenues': 20885000000.0,
            'net_income': 6624000000.0,
            'eps_basic': 0.79,
            'eps_diluted': 0.78,
            'dividend': 0.20,
            'assets': 112243000000.0,
            'equity': 64121000000.0,
            'cash': 10610000000.0
        })

    def test_msft_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/789019/000119312513160748/msft-20130331.xml')
        self.assert_item(item, {
            'symbol': 'MSFT',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2013-03-31',
            'revenues': 20489000000.0,
            'net_income': 6055000000.0,
            'eps_basic': 0.72,
            'eps_diluted': 0.72,
            'dividend': 0.23,
            'assets': 134105000000.0,
            'equity': 76688000000.0,
            'cash': 5240000000.0
        })

    def test_mu_20121129(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/723125/000072312513000007/mu-20121129.xml')
        self.assert_item(item, {
            'symbol': 'MU',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2012-11-29',
            'revenues': 1834000000.0,
            'net_income': -275000000.0,
            'eps_basic': -0.27,
            'eps_diluted': -0.27,
            'dividend': 0.0,
            'assets': 14067000000.0,
            'equity': 8186000000.0,
            'cash': 2102000000.0
        })

    def test_omx_20110924(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12978/000119312511286448/omx-20110924.xml')
        self.assert_item(item, {
            'symbol': 'OMX',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2011-09-24',
            'revenues': 1774767000.0,
            'net_income': 21518000.0,
            'eps_basic': 0.25,
            'eps_diluted': 0.25,
            'dividend': 0.0,
            'assets': 4002981000.0,
            'equity': 657636000.0,
            'cash': 485426000.0
        })

    def test_omx_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12978/000119312512077611/omx-20111231.xml')
        self.assert_item(item, {
            'symbol': 'OMX',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2011-12-31',
            'revenues': 7121167000.0,
            'net_income': 32771000.0,
            'eps_basic': 0.38,
            'eps_diluted': 0.38,
            'dividend': 0.0,
            'assets': 4069275000.0,
            'equity': 568993000.0,
            'cash': 427111000.0
        })

    def test_omx_20121229(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12978/000119312513073972/omx-20121229.xml')
        self.assert_item(item, {
            'symbol': 'OMX',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2012-12-29',
            'revenues': 6920384000.0,
            'net_income': 414694000.0,
            'eps_basic': 4.79,
            'eps_diluted': 4.74,
            'dividend': 0.0,
            'assets': 3784315000.0,
            'equity': 1034373000.0,
            'cash': 495056000.0
        })

    def test_strza_20121231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1507934/000150793413000015/strza-20121231.xml')
        self.assert_item(item, {
            'symbol': 'STRZA',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2012-12-31',
            'revenues': 1630696000.0,
            'net_income': 254484000.0,
            'eps_basic': None,
            'eps_diluted': None,
            'dividend': 0.0,
            'assets': 2176050000.0,
            'equity': 1302144000.0,
            'cash': 749774000.0
        })

    def test_tsla_20110630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1318605/000119312511221497/tsla-20110630.xml')
        self.assert_item(item, {
            'symbol': 'TSLA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2011-06-30',
            'revenues': 58171000.0,
            'net_income': -58903000.0,
            'eps_basic': -0.60,
            'eps_diluted': -0.60,
            'dividend': 0.0,
            'assets': 646155000.0,
            'equity': 348452000.0,
            'cash': 319380000.0
        })

    def test_tsla_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1318605/000119312512137560/tsla-20111231.xml')
        self.assert_item(item, {
            'symbol': 'TSLA',
            'amend': True,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2011-12-31',
            'revenues': 204242000.0,
            'net_income': -254411000.0,
            'eps_basic': -2.53,
            'eps_diluted': -2.53,
            'dividend': 0.0,
            'assets': 713448000.0,
            'equity': 224045000.0,
            'cash': 255266000.0
        })

    def test_tsla_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1318605/000119312513327916/tsla-20130630.xml')
        self.assert_item(item, {
            'symbol': 'TSLA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2013-06-30',
            'revenues': 405139000.0,
            'net_income': -30502000.0,
            'eps_basic': -0.26,
            'eps_diluted': -0.26,
            'dividend': 0.0,
            'assets': 1887844000.0,
            'equity': 629426000.0,
            'cash': 746057000.0
        })

    def test_xom_20110331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/34088/000119312511127973/xom-20110331.xml')
        self.assert_item(item, {
            'symbol': 'XOM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2011-03-31',
            'revenues': 114004000000.0,
            'net_income': 10650000000.0,
            'eps_basic': 2.14,
            'eps_diluted': 2.14,
            'dividend': 0.44,
            'assets': 319533000000.0,
            'equity': 157531000000.0,
            'cash': 12833000000.0
        })

    def test_xom_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/34088/000119312512078102/xom-20111231.xml')
        self.assert_item(item, {
            'symbol': 'XOM',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2011-12-31',
            'revenues': 467029000000.0,
            'net_income': 41060000000.0,
            'eps_basic': 8.43,
            'eps_diluted': 8.42,
            'dividend': 1.85,
            'assets': 331052000000.0,
            'equity': 160744000000.0,
            'cash': 12664000000.0
        })

    def test_xom_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/34088/000003408813000035/xom-20130630.xml')
        self.assert_item(item, {
            'symbol': 'XOM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2013-06-30',
            'revenues': 106469000000.0,
            'net_income': 6860000000.0,
            'eps_basic': 1.55,
            'eps_diluted': 1.55,
            'dividend': 0.63,
            'assets': 341615000000.0,
            'equity': 171588000000.0,
            'cash': 4609000000.0
        })

    def test_xray_20091231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/818479/000114420410009164/xray-20091231.xml')
        self.assert_item(item, {
            'symbol': 'XRAY',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2009-12-31',
            'revenues': 2159916000.0,
            'net_income': 274258000.0,
            'eps_basic': 1.85,
            'eps_diluted': 1.83,
            'dividend': 0.2,
            'assets': 3087932000.0,
            'equity': 1906958000.0,
            'cash': 450348000.0
        })
