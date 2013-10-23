import os
import requests
import urlparse

from scrapy.http.response.xml import XmlResponse

from stockcrawler.loaders import ReportItemLoader
from stockcrawler.tests.base import TestCaseBase


def create_response(file_path):
    with open(file_path) as f:
        body = f.read()
    return XmlResponse('file://%s' % file_path.replace('\\', '/'), body=body)


def download(url, local_path):
    if not os.path.exists(local_path):
        dir_path = os.path.dirname(local_path)
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except OSError:
                pass

        assert os.path.exists(dir_path)

        with open(local_path, 'wb') as f:
            r = requests.get(url, stream=True)
            for chunk in r.iter_content(chunk_size=4096):
                f.write(chunk)


def parse_xml(url):
    url_path = urlparse.urlparse(url).path
    local_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sample_data', url_path[1:])
    download(url, local_path)
    response = create_response(local_path)
    loader = ReportItemLoader(response=response)
    return loader.load_item()


class ReportItemLoaderTest(TestCaseBase):

    def test_a_20110131(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1090872/000110465911013291/a-20110131.xml')
        self.assert_item(item, {
            'symbol': 'A',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2011-01-31',
            'revenues': 1519000000.0,
            'net_income': 193000000.0,
            'eps_basic': 0.56,
            'eps_diluted': 0.54,
            'dividend': 0.0,
            'assets': 8044000000.0,
            'equity': 3339000000.0,
            'cash': 2638000000.0
        })

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

    def test_aes_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/874761/000119312510111183/aes-20100331.xml')
        self.assert_item(item, {
            'symbol': 'AES',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2010-03-31',
            'revenues': 4112000000.0,
            'net_income': 187000000.0,
            'eps_basic': 0.27,
            'eps_diluted': 0.27,
            'dividend': 0.0,
            'assets': 41882000000.0,
            'equity': 10536000000.0,
            'cash': 3392000000.0
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

    def test_chtr_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1091667/000109166712000026/chtr-20111231.xml')
        self.assert_item(item, {
            'symbol': 'CHTR',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2011-12-31',
            'revenues': 7204000000.0,
            'net_income': -369000000.0,
            'eps_basic': -3.39,
            'eps_diluted': -3.39,
            'dividend': 0.0,
            'assets': 15605000000,
            'equity': 409000000,
            'cash': 2000000
        })

    def test_disca_20090630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1437107/000095012309029613/disca-20090630.xml')
        self.assert_item(item, {
            'symbol': 'DISCA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2009-06-30',
            'revenues': 881000000.0,
            'net_income': 183000000.0,
            'eps_basic': 0.43,
            'eps_diluted': 0.43,
            'dividend': 0.0,
            'assets': 10696000000.0,
            'equity': 5918000000.0,
            'cash': 339000000.0
        })

    def test_disca_20090930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1437107/000095012309056946/disca-20090930.xml')
        self.assert_item(item, {
            'symbol': 'DISCA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2009-09-30',
            'revenues': 854000000.0,
            'net_income': 95000000.0,
            'eps_basic': 0.22,
            'eps_diluted': 0.22,
            'dividend': 0.0,
            'assets': 10741000000.0,
            'equity': 6042000000.0,
            'cash': 401000000.0
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

    def test_dtv_20110331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1465112/000104746911004655/dtv-20110331.xml')
        self.assert_item(item, {
            'symbol': 'DTV',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2011-03-31',
            'revenues': 6319000000.0,
            'net_income': 674000000.0,
            'eps_basic': 0.85,
            'eps_diluted': 0.85,
            'dividend': 0.0,
            'assets': 20593000000.0,
            'equity': -902000000.0,
            'cash': 4295000000.0
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

    def test_fast_20090630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/815556/000119312509154691/fast-20090630.xml')
        self.assert_item(item, {
            'symbol': 'FAST',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2009-06-30',
            'revenues': 474894000.0,
            'net_income': 43538000.0,
            'eps_basic': 0.29,
            'eps_diluted': 0.29,
            'dividend': 0.0,
            'assets': 1328684000.0,
            'equity': 1186845000.0,
            'cash': 173667000.0
        })

    def test_fast_20090930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/815556/000119312509212481/fast-20090930.xml')
        self.assert_item(item, {
            'symbol': 'FAST',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2009-09-30',
            'revenues': 489339000.0,
            'net_income': 47589000.0,
            'eps_basic': 0.32,
            'eps_diluted': 0.32,
            'dividend': 0.0,
            'assets': 1337764000.0,
            'equity': 1185140000.0,
            'cash': 193744000.0
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

    def test_gmcr_20110625(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/909954/000119312511214253/gmcr-20110630.xml')
        self.assert_item(item, {
            'symbol': 'GMCR',
            'amend': False,  # it's actually amended, but not marked in XML
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2011-06-25',
            'revenues': 717210000.0,
            'net_income': 56348000.0,
            'eps_basic': 0.38,
            'eps_diluted': 0.37,
            'dividend': 0.0,
            'assets': 2874422000.0,
            'equity': 1816646000.0,
            'cash': 76138000.0
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

    def test_intc_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/50863/000119312512075534/intc-20111231.xml')
        self.assert_item(item, {
            'symbol': 'INTC',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2011-12-31',
            'revenues': 53999000000.0,
            'net_income': 12942000000.0,
            'eps_basic': 2.46,
            'eps_diluted': 2.39,
            'dividend': 0.7824,
            'assets': 71119000000.0,
            'equity': 45911000000.0,
            'cash': 5065000000.0
        })

    def test_intu_20101031(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/896878/000095012310111135/intu-20101031.xml')
        self.assert_item(item, {
            'symbol': 'INTU',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2010-10-31',
            'revenues': 532000000.0,
            'net_income': -70000000.0,
            'eps_basic': -0.22,
            'eps_diluted': -0.22,
            'dividend': 0.0,
            'assets': 4943000000.0,
            'equity': 2615000000.0,
            'cash': 112000000.0
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

    def test_krft_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1545158/000119312512495570/krft-20120930.xml')
        self.assert_item(item, {
            'symbol': 'KRFT',
            'amend': True,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2012-09-30',
            'revenues': 4606000000.0,
            'net_income': 470000000.0,
            'eps_basic': 0.79,
            'eps_diluted': 0.79,
            'dividend': 0.0,
            'assets': 22284000000.0,
            'equity': 7458000000.0,
            'cash': 244000000.0
        })

    def test_lbtya_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1316631/000119312510111069/lbtya-20100331.xml')
        self.assert_item(item, {
            'symbol': 'LBTYA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2010-03-31',
            'revenues': 2178900000.0,
            'net_income': 736600000.0,
            'eps_basic': 2.75,
            'eps_diluted': 2.75,
            'dividend': 0.0,
            'assets': 33083500000.0,
            'equity': 4066000000.0,
            'cash': 4184200000.0
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

    def test_lltc_20111002(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/791907/000079190711000080/lltc-20111007.xml')
        self.assert_item(item, {
            'symbol': 'LLTC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2011-10-02',
            'revenues': 329920000.0,
            'net_income': 108401000.0,
            'eps_basic': 0.47,
            'eps_diluted': 0.47,
            'dividend': 0.24,
            'assets': 1659341000.0,
            'equity': 543199000.0,
            'cash': 163414000.0
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

    def test_mchp_20120630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/827054/000082705412000230/mchp-20120630.xml')
        self.assert_item(item, {
            'symbol': 'MCHP',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2012-06-30',
            'revenues': 352134000.0,
            'net_income': 78710000.0,
            'eps_basic': 0.41,
            'eps_diluted': 0.39,
            'dividend': 0.35,
            'assets': 3144840000.0,
            'equity': 2017990000.0,
            'cash': 779848000.0
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

    def test_mxim_20110326(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/743316/000144530511000751/mxim-20110422.xml')
        self.assert_item(item, {
            'symbol': 'MXIM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2011-03-26',
            'revenues': 606775000.0,
            'net_income': 136276000.0,
            'eps_basic': 0.46,
            'eps_diluted': 0.45,
            'dividend': 0.21,
            'assets': 3452417000.0,
            'equity': 2465040000.0,
            'cash': 868923000.0
        })

    def test_nflx_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1065280/000106528012000020/nflx-20120930.xml')
        self.assert_item(item, {
            'symbol': 'NFLX',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2012-09-30',
            'revenues': 905089000.0,
            'net_income': 7675000.0,
            'eps_basic': 0.14,
            'eps_diluted': 0.13,
            'dividend': 0.0,
            'assets': 3808833000.0,
            'equity': 716840000.0,
            'cash': 370298000.0
        })

    def test_nvda_20130127(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1045810/000104581013000008/nvda-20130127.xml')
        self.assert_item(item, {
            'symbol': 'NVDA',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2013-01-27',
            'revenues': 4280159000.0,
            'net_income': 562536000.0,
            'eps_basic': 0.91,
            'eps_diluted': 0.9,
            'dividend': 0.075,
            'assets': 6412245000.0,
            'equity': 4827703000.0,
            'cash': 732786000.0
        })

    def test_nws_20090930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1308161/000119312509224062/nws-20090930.xml')
        self.assert_item(item, {
            'symbol': 'NWS',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2009-09-30',
            'revenues': 7199000000.0,
            'net_income': 571000000.0,
            'eps_basic': 0.22,
            'eps_diluted': 0.22,
            'dividend': 0.06,
            'assets': 55316000000.0,
            'equity': 24479000000.0,
            'cash': 7832000000.0
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

    def test_orly_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/898173/000089817313000028/orly-20130331.xml')
        self.assert_item(item, {
            'symbol': 'ORLY',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2013-03-31',
            'revenues': 1585009000.0,
            'net_income': 154329000.0,
            'eps_basic': 1.38,
            'eps_diluted': 1.36,
            'dividend': 0.0,
            'assets': 5789541000.0,
            'equity': 2072525000.0,
            'cash': 205410000.0
        })

    def test_pcar_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/75362/000119312510108284/pcar-20100331.xml')
        self.assert_item(item, {
            'symbol': 'PCAR',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2010-03-31',
            'revenues': 2230700000.0,
            'net_income': 68300000.0,
            'eps_basic': 0.19,
            'eps_diluted': 0.19,
            'dividend': 0.09,
            'assets': 13990000000.0,
            'equity': 5092600000.0,
            'cash': 1854700000.0
        })

    def test_regn_20100630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/872589/000120677410001689/regn-20100630.xml')
        self.assert_item(item, {
            'symbol': 'REGN',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2010-06-30',
            'revenues': 115886000.0,
            'net_income': -25474000.0,
            'eps_basic': -0.31,
            'eps_diluted': -0.31,
            'dividend': 0.0,
            'assets': 790641000.0,
            'equity': 371216000.0,
            'cash': 112000000.0
        })

    def test_sbac_20110331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1034054/000119312511130220/sbac-20110331.xml')
        self.assert_item(item, {
            'symbol': 'SBAC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2011-03-31',
            'revenues': 167749000.0,
            'net_income': -34251000.0,
            'eps_basic': -0.3,
            'eps_diluted': -0.3,
            'dividend': 0.0,
            'assets': 3466258000.0,
            'equity': 213078000.0,
            'cash': 95104000.0
        })

    def test_shld_20101030(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1310067/000119312510263486/shld-20101030.xml')
        self.assert_item(item, {
            'symbol': 'SHLD',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2010-10-30',
            'revenues': 9678000000.0,
            'net_income': -218000000.0,
            'eps_basic': -1.98,
            'eps_diluted': -1.98,
            'dividend': 0.0,
            'assets': 26045000000.0,
            'equity': 8378000000.0,
            'cash': 790000000.0
        })

    def test_sial_20101231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/90185/000119312511028579/sial-20101231.xml')
        self.assert_item(item, {
            'symbol': 'SIAL',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'end_date': '2010-12-31',
            'revenues': 2271000000.0,
            'net_income': 384000000.0,
            'eps_basic': 3.17,
            'eps_diluted': 3.12,
            'dividend': 0.0,
            'assets': 3014000000.0,
            'equity': 1976000000.0,
            'cash': 569000000.0
        })

    def test_siri_20100630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/908937/000095012310074081/siri-20100630.xml')
        self.assert_item(item, {
            'symbol': 'SIRI',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2010-06-30',
            'revenues': 699761000.0,
            'net_income': 15272000.0,
            'eps_basic': 0.0,
            'eps_diluted': 0.0,
            'dividend': 0.0,
            'assets': 7200932000.0,
            'equity': 180428000.0,
            'cash': 258854000.0
        })

    def test_siri_20120331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/908937/000090893712000003/siri-20120331.xml')
        self.assert_item(item, {
            'symbol': 'SIRI',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2012-03-31',
            'revenues': 804722000.0,
            'net_income': 107774000.0,
            'eps_basic': 0.03,
            'eps_diluted': 0.02,
            'dividend': 0.0,
            'assets': 7501724000.0,
            'equity': 849579000.0,
            'cash': 746576000.0
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

    def test_stx_20120928(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1137789/000110465912072744/stx-20120928.xml')
        self.assert_item(item, {
            'symbol': 'STX',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2012-09-28',
            'revenues': 3732000000.0,
            'net_income': 582000000.0,
            'eps_basic': 1.48,
            'eps_diluted': 1.42,
            'dividend': 0.32,
            'assets': 9522000000.0,
            'equity': 3535000000.0,
            'cash': 1894000000.0
        })

    def test_stx_20121228(self):
        # 'stx-20120928' is misnamed
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1137789/000110465913005497/stx-20120928.xml')
        self.assert_item(item, {
            'symbol': 'STX',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'end_date': '2012-12-28',
            'revenues': 3668000000.0,
            'net_income': 492000000.0,
            'eps_basic': 1.33,
            'eps_diluted': 1.3,
            'dividend': 0.7,
            'assets': 8742000000,
            'equity': 2925000000.0,
            'cash': 1383000000.0
        })

    def test_symc_20130628(self):
        # 'symc-20140628.xml' is misnamed
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/849399/000119312513312695/symc-20140628.xml')
        self.assert_item(item, {
            'symbol': 'SYMC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2013-06-28',
            'revenues': 1709000000.0,
            'net_income': 157000000.0,
            'eps_basic': 0.23,
            'eps_diluted': 0.22,
            'dividend': 0.15,
            'assets': 13151000000.0,
            'equity': 5497000000.0,
            'cash': 3749000000.0
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

    def test_via_20090930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1339947/000119312509221448/via-20090930.xml')
        self.assert_item(item, {
            'symbol': 'VIA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2009-09-30',
            'revenues': 3317000000.0,
            'net_income': 463000000.0,
            'eps_basic': 0.76,
            'eps_diluted': 0.76,
            'dividend': 0.0,
            'assets': 21307000000.0,
            'equity': 8044000000.0,
            'cash': 249000000.0
        })

    def test_via_20120630(self):
        # 'via-20120401.xml' is misnamed
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1339947/000119312512333732/via-20120401.xml')
        self.assert_item(item, {
            'symbol': 'VIA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2012-06-30',
            'revenues': 3241000000.0,
            'net_income': 534000000.0,
            'eps_basic': 1.02,
            'eps_diluted': 1.01,
            'dividend': 0.275,
            'assets': 21958000000.0,
            'equity': 7473000000.0,
            'cash': 774000000.0
        })

    def test_vrsk_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1442145/000119312512441544/vrsk-20120930.xml')
        self.assert_item(item, {
            'symbol': 'VRSK',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'end_date': '2012-09-30',
            'revenues': 398863000.0,
            'net_income': 82911000.0,
            'eps_basic': 0.5,
            'eps_diluted': 0.48,
            'dividend': 0.0,
            'assets': 2303433000.0,
            'equity': 142048000.0,
            'cash': 97770000.0
        })

    def test_wfm_20120115(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/865436/000144530512000434/wfm-20120115.xml')
        self.assert_item(item, {
            'symbol': 'WFM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'end_date': '2012-01-15',
            'revenues': 3390940000.0,
            'net_income': 118327000.0,
            'eps_basic': 0.66,
            'eps_diluted': 0.65,
            'dividend': 0.14,
            'assets': 4528241000.0,
            'equity': 3182747000.0,
            'cash': 529954000.0
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
