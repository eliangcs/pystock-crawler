import os
import requests
import urlparse

from scrapy.http.response.xml import XmlResponse

from pystock_crawler.loaders import ReportItemLoader
from pystock_crawler.tests.base import SAMPLE_DATA_DIR, TestCaseBase


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
    local_path = os.path.join(SAMPLE_DATA_DIR, url_path[1:])
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
            'fiscal_year': 2011,
            'end_date': '2011-01-31',
            'revenues': 1519000000,
            'op_income': 211000000,
            'net_income': 193000000,
            'eps_basic': 0.56,
            'eps_diluted': 0.54,
            'dividend': 0.0,
            'assets': 8044000000,
            'cur_assets': 4598000000,
            'cur_liab': 1406000000,
            'equity': 3339000000,
            'cash': 2638000000,
            'cash_flow_op': 120000000,
            'cash_flow_inv': 1500000000,
            'cash_flow_fin': -1634000000
        })

    def test_aa_20120630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/4281/000119312512317135/aa-20120630.xml')
        self.assert_item(item, {
            'symbol': 'AA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2012,
            'end_date': '2012-06-30',
            'revenues': 5963000000,
            'op_income': None,  # Missing value
            'net_income': -2000000,
            'eps_basic': None,  # EPS is 0 actually, but got no data in XML
            'eps_diluted': None,
            'dividend': 0.03,
            'assets': 39498000000,
            'cur_assets': 7767000000,
            'cur_liab': 6151000000,
            'equity': 16914000000,
            'cash': 1712000000,
            'cash_flow_op': 301000000,
            'cash_flow_inv': -704000000,
            'cash_flow_fin': 196000000
        })

    def test_aapl_20100626(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/320193/000119312510162840/aapl-20100626.xml')
        self.assert_item(item, {
            'symbol': 'AAPL',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2010,
            'end_date': '2010-06-26',
            'revenues': 15700000000,
            'op_income': 4234000000,
            'net_income': 3253000000,
            'eps_basic': 3.57,
            'eps_diluted': 3.51,
            'dividend': 0.0,
            'assets': 64725000000,
            'cur_assets': 36033000000,
            'cur_liab': 15612000000,
            'equity': 43111000000,
            'cash': 9705000000,
            'cash_flow_op': 12912000000,
            'cash_flow_inv': -9471000000,
            'cash_flow_fin': 1001000000
        })

    def test_aapl_20110326(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/320193/000119312511104388/aapl-20110326.xml')
        self.assert_item(item, {
            'symbol': 'AAPL',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2011,
            'end_date': '2011-03-26',
            'revenues': 24667000000,
            'net_income': 5987000000,
            'op_income': 7874000000,
            'eps_basic': 6.49,
            'eps_diluted': 6.40,
            'dividend': 0.0,
            'assets': 94904000000,
            'cur_assets': 46997000000,
            'cur_liab': 24327000000,
            'equity': 61477000000,
            'cash': 15978000000,
            'cash_flow_op': 15992000000,
            'cash_flow_inv': -12251000000,
            'cash_flow_fin': 976000000
        })

    def test_aapl_20120929(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/320193/000119312512444068/aapl-20120929.xml')
        self.assert_item(item, {
            'symbol': 'AAPL',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2012,
            'end_date': '2012-09-29',
            'revenues': 156508000000,
            'op_income': 55241000000,
            'net_income': 41733000000,
            'eps_basic': 44.64,
            'eps_diluted': 44.15,
            'dividend': 2.65,
            'assets': 176064000000,
            'cur_assets': 57653000000,
            'cur_liab': 38542000000,
            'equity': 118210000000,
            'cash': 10746000000,
            'cash_flow_op': 50856000000,
            'cash_flow_inv': -48227000000,
            'cash_flow_fin': -1698000000
        })

    def test_aes_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/874761/000119312510111183/aes-20100331.xml')
        self.assert_item(item, {
            'symbol': 'AES',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2010-03-31',
            'revenues': 4112000000,
            'op_income': None,  # Missing value
            'net_income': 187000000,
            'eps_basic': 0.27,
            'eps_diluted': 0.27,
            'dividend': 0.0,
            'assets': 41882000000,
            'cur_assets': 10460000000,
            'cur_liab': 6894000000,
            'equity': 10536000000,
            'cash': 3392000000,
            'cash_flow_op': 684000000,
            'cash_flow_inv': -595000000,
            'cash_flow_fin': 1515000000
        })

    def test_adbe_20060914(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/796343/000110465906066129/adbe-20060914.xml')

        # Old document is not supported
        self.assertFalse(item)

    def test_adbe_20090227(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/796343/000079634309000021/adbe-20090227.xml')
        self.assert_item(item, {
            'symbol': 'ADBE',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2009,
            'end_date': '2009-02-27',
            'revenues': 786390000,
            'op_income': 207916000,
            'net_income': 156435000,
            'eps_basic': 0.3,
            'eps_diluted': 0.3,
            'dividend': 0.0,
            'assets': 5887596000,
            'cur_assets': 2868991000,
            'cur_liab': 636865000,
            'equity': 4611160000,
            'cash': 1148925000,
            'cash_flow_op': 365743000,
            'cash_flow_inv': -131562000,
            'cash_flow_fin': 28675000
        })

    def test_agn_20101231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/850693/000119312511050632/agn-20101231.xml')
        self.assert_item(item, {
            'symbol': 'AGN',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2010,
            'end_date': '2010-12-31',
            'revenues': 4919400000,
            'op_income': 258600000,
            'net_income': 600000,
            'eps_basic': 0.0,
            'eps_diluted': 0.0,
            'dividend': 0.2,
            'assets': 8308100000,
            'cur_assets': 3993700000,
            'cur_liab': 1528400000,
            'equity': 4781100000,
            'cash': 1991200000,
            'cash_flow_op': 463900000,
            'cash_flow_inv': -977200000,
            'cash_flow_fin': 563000000
        })

    def test_aig_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/5272/000104746913008075/aig-20130630.xml')
        self.assert_item(item, {
            'symbol': 'AIG',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-30',
            'revenues': 17315000000,
            'net_income': 2731000000,
            'op_income': None,
            'eps_basic': 1.85,
            'eps_diluted': 1.84,
            'dividend': 0.0,
            'assets': 537438000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 98155000000,
            'cash': 1762000000,
            'cash_flow_op': 1674000000,
            'cash_flow_inv': 6071000000,
            'cash_flow_fin': -7055000000
        })

    def test_aiv_20110630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/922864/000095012311070591/aiv-20110630.xml')
        self.assert_item(item, {
            'symbol': 'AIV',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2011,
            'end_date': '2011-06-30',
            'revenues': 281035000,
            'op_income': 49791000,
            'net_income': -33177000,
            'eps_basic': -0.28,
            'eps_diluted': -0.28,
            'dividend': 0.12,
            'assets': 7164972000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 1241336000,
            'cash': 85324000,
            'cash_flow_op': 95208000,
            'cash_flow_inv': -33538000,
            'cash_flow_fin': -87671000
        })

    def test_all_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/899051/000110465913035969/all-20130331.xml')
        self.assert_item(item, {
            'symbol': 'ALL',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2013-03-31',
            'revenues': 8463000000,
            'op_income': None,
            'net_income': 709000000,
            'eps_basic': 1.49,
            'eps_diluted': 1.47,
            'dividend': 0.25,
            'assets': 126612000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 20619000000,
            'cash': 820000000,
            'cash_flow_op': 740000000,
            'cash_flow_inv': 136000000,
            'cash_flow_fin': -862000000
        })

    def test_apa_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/6769/000119312512457830/apa-20120930.xml')
        self.assert_item(item, {
            'symbol': 'APA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-30',
            'revenues': 4179000000,
            'op_income': None,
            'net_income': 161000000,
            'eps_basic': 0.41,
            'eps_diluted': 0.41,
            'dividend': 0.17,
            'assets': 58810000000,
            'cur_assets': 5044000000,
            'cur_liab': 5390000000,
            'equity': 30714000000,
            'cash': 318000000,
            'cash_flow_op': 6422000000,
            'cash_flow_inv': -10560000000,
            'cash_flow_fin': 4161000000
        })

    def test_axp_20100930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/4962/000095012310100214/axp-20100930.xml')
        self.assert_item(item, {
            'symbol': 'AXP',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2010,
            'end_date': '2010-09-30',
            'revenues': 6660000000,
            'op_income': 1640000000,
            'net_income': 1093000000,
            'eps_basic': 0.91,
            'eps_diluted': 0.9,
            'dividend': 0.18,
            'assets': 146056000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 15920000000,
            'cash': 21341000000,
            'cash_flow_op': 7227000000,
            'cash_flow_inv': 5298000000,
            'cash_flow_fin': -7885000000
        })

    def test_axp_20120630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/4962/000119312512332179/axp-20120630.xml')
        self.assert_item(item, {
            'symbol': 'AXP',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2012,
            'end_date': '2012-06-30',
            'revenues': 7504000000,
            'op_income': None,
            'net_income': 1339000000,
            'eps_basic': 1.16,
            'eps_diluted': 1.15,
            'dividend': 0.2,
            'assets': 148128000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 19267000000,
            'cash': 22072000000,
            'cash_flow_op': 6742000000,
            'cash_flow_inv': -1771000000,
            'cash_flow_fin': -7786000000
        })

    def test_axp_20121231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/4962/000119312513070554/axp-20121231.xml')
        self.assert_item(item, {
            'symbol': 'AXP',
            'amend': True,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2012,
            'end_date': '2012-12-31',
            'revenues': 29592000000,
            'op_income': None,
            'net_income': 4482000000,
            'eps_basic': 3.91,
            'eps_diluted': 3.89,
            'dividend': 0.8,
            'assets': 153140000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 18886000000,
            'cash': 22250000000,
            'cash_flow_op': 7082000000,
            'cash_flow_inv': -6545000000,
            'cash_flow_fin': -3268000000
        })

    def test_axp_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/4962/000119312513180601/axp-20130331.xml')
        self.assert_item(item, {
            'symbol': 'AXP',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2013-03-31',
            'revenues': 7384000000,
            'op_income': None,
            'net_income': 1280000000,
            'eps_basic': 1.15,
            'eps_diluted': 1.15,
            'dividend': 0.2,
            'assets': 156855000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 19290000000,
            'cash': 27964000000,
            'cash_flow_op': 7547000000,
            'cash_flow_inv': 32000000,
            'cash_flow_fin': -1830000000
        })

    def test_ba_20091231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12927/000119312510024406/ba-20091231.xml')
        self.assert_item(item, {
            'symbol': 'BA',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2009,
            'end_date': '2009-12-31',
            'revenues': 68281000000,
            'op_income': 2096000000,
            'net_income': 1312000000,
            'eps_basic': 1.86,
            'eps_diluted': 1.84,
            'dividend': 1.68,
            'assets': 62053000000,
            'cur_assets': 35275000000,
            'cur_liab': 32883000000,
            'equity': 2225000000,
            'cash': 9215000000,
            'cash_flow_op': 5603000000,
            'cash_flow_inv': -3794000000,
            'cash_flow_fin': 4094000000
        })

    def test_ba_20110930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12927/000119312511281613/ba-20110930.xml')
        self.assert_item(item, {
            'symbol': 'BA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2011,
            'end_date': '2011-09-30',
            'revenues': 17727000000,
            'op_income': 1714000000,
            'net_income': 1098000000,
            'eps_basic': 1.47,
            'eps_diluted': 1.46,
            'dividend': 0.42,
            'assets': 74163000000,
            'cur_assets': 46347000000,
            'cur_liab': 37593000000,
            'equity': 6061000000,
            'cash': 5954000000,
            'cash_flow_op': 1092000000,
            'cash_flow_inv': 856000000,
            'cash_flow_fin': -1354000000
        })

    def test_ba_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12927/000001292713000023/ba-20130331.xml')
        self.assert_item(item, {
            'symbol': 'BA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2013-03-31',
            'revenues': 18893000000,
            'op_income': 1528000000,
            'net_income': 1106000000,
            'eps_basic': 1.45,
            'eps_diluted': 1.44,
            'dividend': 0.49,
            'assets': 90447000000,
            'cur_assets': 59490000000,
            'cur_liab': 45666000000,
            'equity': 7560000000,
            'cash': 8335000000,
            'cash_flow_op': 524000000,
            'cash_flow_inv': -814000000,
            'cash_flow_fin': -1705000000
        })

    def test_bbt_20110930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/92230/000119312511304459/bbt-20110930.xml')
        self.assert_item(item, {
            'symbol': 'BBT',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2011,
            'end_date': '2011-09-30',
            'revenues': 2440000000,
            'op_income': None,
            'net_income': 366000000,
            'eps_basic': 0.52,
            'eps_diluted': 0.52,
            'dividend': 0.16,
            'assets': 167677000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 17541000000,
            'cash': 1312000000,
            'cash_flow_op': 4348000000,
            'cash_flow_inv': -10838000000,
            'cash_flow_fin': 8509000000
        })

    def test_bk_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1390777/000119312510112944/bk-20100331.xml')
        self.assert_item(item, {
            'symbol': 'BK',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2010-03-31',
            'revenues': 883000000,
            'op_income': None,
            'net_income': 559000000,
            'eps_basic': 0.46,
            'eps_diluted': 0.46,
            'dividend': 0.09,
            'assets': 220551000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 30455000000,
            'cash': 3307000000,
            'cash_flow_op': 1191000000,
            'cash_flow_inv': 512000000,
            'cash_flow_fin': -2126000000
        })

    def test_blk_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1364742/000119312513326890/blk-20130630.xml')
        self.assert_item(item, {
            'symbol': 'BLK',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-30',
            'revenues': 2482000000,
            'op_income': 849000000,
            'net_income': 729000000,
            'eps_basic': 4.27,
            'eps_diluted': 4.19,
            'dividend': 1.68,
            'assets': 193745000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 25755000000,
            'cash': 3668000000,
            'cash_flow_op': 1330000000,
            'cash_flow_inv': 10000000,
            'cash_flow_fin': -2193000000
        })

    def test_c_20090630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/831001/000104746909007400/c-20090630.xml')
        self.assert_item(item, {
            'symbol': 'C',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2009,
            'end_date': '2009-06-30',
            'revenues': 29969000000,
            'net_income': 4279000000,
            'op_income': None,
            'eps_basic': 0.49,
            'eps_diluted': 0.49,
            'dividend': 0.0,
            'assets': 1848533000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 154168000000,
            'cash': 26915000000,
            'cash_flow_op': -20737000000,
            'cash_flow_inv': 16457000000,
            'cash_flow_fin': 959000000
        })

    def test_cbs_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/813828/000104746910004823/cbs-20100331.xml')
        self.assert_item(item, {
            'symbol': 'CBS',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2010-03-31',
            'revenues': 3530900000,
            'op_income': 153400000,
            'net_income': -26200000,
            'eps_basic': -0.04,
            'eps_diluted': -0.04,
            'dividend': 0.05,
            'assets': 26756100000,
            'cur_assets': 5705200000,
            'cur_liab': 4712300000,
            'equity': 9046100000,
            'cash': 872700000,
            'cash_flow_op': 700700000,
            'cash_flow_inv': -73600000,
            'cash_flow_fin': -471100000
        })

    def test_cbs_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/813828/000104746912001373/cbs-20111231.xml')
        self.assert_item(item, {
            'symbol': 'CBS',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2011-12-31',
            'revenues': 14245000000,
            'op_income': 2529000000,
            'net_income': 1305000000,
            'eps_basic': 1.97,
            'eps_diluted': 1.92,
            'dividend': 0.35,
            'assets': 26197000000,
            'cur_assets': 5543000000,
            'cur_liab': 3933000000,
            'equity': 9908000000,
            'cash': 660000000,
            'cash_flow_op': 1749000000,
            'cash_flow_inv': -389000000,
            'cash_flow_fin': -1180000000
        })

    def test_cbs_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/813828/000104746913007929/cbs-20130630.xml')
        self.assert_item(item, {
            'symbol': 'CBS',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-30',
            'revenues': 3699000000,
            'op_income': 838000000,
            'net_income': 472000000,
            'eps_basic': 0.78,
            'eps_diluted': 0.76,
            'dividend': 0.12,
            'assets': 25693000000,
            'cur_assets': 4770000000,
            'cur_liab': 3825000000,
            'equity': 9601000000,
            'cash': 282000000,
            'cash_flow_op': 1051000000,
            'cash_flow_inv': -230000000,
            'cash_flow_fin': -1247000000
        })

    def test_cce_20101001(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1491675/000119312510239952/cce-20101001.xml')
        self.assert_item(item, {
            'symbol': 'CCE',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2010,
            'end_date': '2010-10-01',
            'revenues': 1681000000,
            'op_income': 244000000,
            'net_income': 208000000,
            'eps_basic': 0.61,
            'eps_diluted': 0.61,
            'dividend': 0.0,
            'assets': 8457000000,
            'cur_assets': 3145000000,
            'cur_liab': 2154000000,
            'equity': 3277000000,
            'cash': 476000000,
            'cash_flow_op': 620000000,
            'cash_flow_inv': -705000000,
            'cash_flow_fin': 178000000
        })

    def test_cce_20101231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1491675/000119312511033197/cce-20101231.xml')
        self.assert_item(item, {
            'symbol': 'CCE',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2010,
            'end_date': '2010-12-31',
            'revenues': 6714000000,
            'op_income': 810000000,
            'net_income': 624000000,
            'eps_basic': 1.84,
            'eps_diluted': 1.83,
            'dividend': 0.12,
            'assets': 8596000000,
            'cur_assets': 2230000000,
            'cur_liab': 1942000000,
            'equity': 3143000000,
            'cash': 321000000,
            'cash_flow_op': 825000000,
            'cash_flow_inv': -739000000,
            'cash_flow_fin': -144000000
        })

    def test_cci_20091231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1051470/000119312510031419/cci-20091231.xml')
        self.assert_item(item, {
            'symbol': 'CCI',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2009,
            'end_date': '2009-12-31',
            'revenues': 1685407000,
            'op_income': 433991000,
            'net_income': -135138000,
            'eps_basic': -0.47,
            'eps_diluted': -0.47,
            'dividend': 0.0,
            'assets': 10956606000,
            'cur_assets': 1196033000,
            'cur_liab': 754105000,
            'equity': 2936085000,
            'cash': 766146000,
            'cash_flow_op': 571256000,
            'cash_flow_inv': -172145000,
            'cash_flow_fin': 214396000
        })

    def test_ccmm_20110630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1091667/000109166711000103/ccmm-20110630.xml')
        self.assert_item(item, {
            'symbol': 'CCMM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2011,
            'end_date': '2011-06-30',
            'revenues': 1791000000,
            'op_income': 270000000,
            'net_income': -107000000,
            'eps_basic': -0.98,
            'eps_diluted': -0.98,
            'dividend': 0.0,
            'assets': None,
            'cur_assets': None,  # Seems the source filing got the wrong context date on balance sheet
            'cur_liab': None,
            'equity': None,
            'cash': 194000000,
            'cash_flow_op': 907000000,
            'cash_flow_inv': -694000000,
            'cash_flow_fin': -51000000
        })

    def test_chtr_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1091667/000109166712000026/chtr-20111231.xml')
        self.assert_item(item, {
            'symbol': 'CHTR',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2011-12-31',
            'revenues': 7204000000,
            'op_income': 1041000000,
            'net_income': -369000000,
            'eps_basic': -3.39,
            'eps_diluted': -3.39,
            'dividend': 0.0,
            'assets': 15605000000,
            'cur_assets': 370000000,
            'cur_liab': 1153000000,
            'equity': 409000000,
            'cash': 2000000,
            'cash_flow_op': 1737000000,
            'cash_flow_inv': -1367000000,
            'cash_flow_fin': -373000000
        })

    def test_ci_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/701221/000110465913036475/ci-20130331.xml')
        self.assert_item(item, {
            'symbol': 'CI',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2013-03-31',
            'revenues': 8183000000,
            'op_income': None,
            'net_income': 57000000,
            'eps_basic': 0.2,
            'eps_diluted': 0.2,
            'dividend': 0.04,
            'assets': 54939000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 9660000000,
            'cash': 3306000000,
            'cash_flow_op': -805000000,
            'cash_flow_inv': 962000000,
            'cash_flow_fin': 185000000
        })

    def test_cit_20100630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1171825/000089109210003376/cit-20100331.xml')
        self.assert_item(item, {
            'symbol': 'CIT',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2010,
            'end_date': '2010-06-30',
            'revenues': 669500000,
            'op_income': None,
            'net_income': 142100000,
            'eps_basic': 0.71,
            'eps_diluted': 0.71,
            'dividend': 0.0,
            'assets': 54916800000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 8633900000,
            'cash': 1060700000,
            'cash_flow_op': 178100000,
            'cash_flow_inv': 7122800000,
            'cash_flow_fin': -6218700000
        })

    def test_csc_20120928(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/23082/000002308212000073/csc-20120928.xml')
        self.assert_item(item, {
            'symbol': 'CSC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2012-09-28',
            'revenues': 3854000000,
            'op_income': 298000000,
            'net_income': 130000000,
            'eps_basic': 0.84,
            'eps_diluted': 0.83,
            'dividend': 0.2,
            'assets': 11649000000,
            'cur_assets': 5468000000,
            'cur_liab': 4015000000,
            'equity': 2885000000,
            'cash': 1850000000,
            'cash_flow_op': 665000000,
            'cash_flow_inv': -366000000,
            'cash_flow_fin': 469000000
        })

    def test_disca_20090630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1437107/000095012309029613/disca-20090630.xml')
        self.assert_item(item, {
            'symbol': 'DISCA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2009,
            'end_date': '2009-06-30',
            'revenues': 881000000,
            'op_income': 486000000,
            'net_income': 183000000,
            'eps_basic': 0.43,
            'eps_diluted': 0.43,
            'dividend': 0.0,
            'assets': 10696000000,
            'cur_assets': 1331000000,
            'cur_liab': 1227000000,
            'equity': 5918000000,
            'cash': 339000000,
            'cash_flow_op': 320000000,
            'cash_flow_inv': 288000000,
            'cash_flow_fin': -371000000
        })

    def test_disca_20090930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1437107/000095012309056946/disca-20090930.xml')
        self.assert_item(item, {
            'symbol': 'DISCA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2009,
            'end_date': '2009-09-30',
            'revenues': 854000000,
            'op_income': 215000000,
            'net_income': 95000000,
            'eps_basic': 0.22,
            'eps_diluted': 0.22,
            'dividend': 0.0,
            'assets': 10741000000,
            'cur_assets': 1417000000,
            'cur_liab': 762000000,
            'equity': 6042000000,
            'cash': 401000000,
            'cash_flow_op': 358000000,
            'cash_flow_inv': 279000000,
            'cash_flow_fin': -343000000
        })

    def test_dltr_20130504(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/935703/000093570313000029/dltr-20130504.xml')
        self.assert_item(item, {
            'symbol': 'DLTR',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2013-05-04',
            'revenues': 1865800000,
            'op_income': 216600000,
            'net_income': 133500000,
            'eps_basic': 0.6,
            'eps_diluted': 0.59,
            'dividend': 0.0,
            'assets': 2811800000,
            'cur_assets': 1489800000,
            'cur_liab': 663000000,
            'equity': 1739700000,
            'cash': 383300000,
            'cash_flow_op': 129300000,
            'cash_flow_inv': -88200000,
            'cash_flow_fin': -57400000
        })

    def test_dtv_20110331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1465112/000104746911004655/dtv-20110331.xml')
        self.assert_item(item, {
            'symbol': 'DTV',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2011,
            'end_date': '2011-03-31',
            'revenues': 6319000000,
            'op_income': 1155000000,
            'net_income': 674000000,
            'eps_basic': 0.85,
            'eps_diluted': 0.85,
            'dividend': 0.0,
            'assets': 20593000000,
            'cur_assets': 6938000000,
            'cur_liab': 4125000000,
            'equity': -902000000,
            'cash': 4295000000,
            'cash_flow_op': 1309000000,
            'cash_flow_inv': -544000000,
            'cash_flow_fin': 2028000000
        })

    def test_ebay_20100630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1065088/000119312510164115/ebay-20100630.xml')
        self.assert_item(item, {
            'symbol': 'EBAY',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2010,
            'end_date': '2010-06-30',
            'revenues': 2215379000,
            'op_income': 484565000,
            'net_income': 412192000,
            'eps_basic': 0.31,
            'eps_diluted': 0.31,
            'dividend': 0.0,
            'assets': 18747584000,
            'cur_assets': 8675313000,
            'cur_liab': 3564261000,
            'equity': 14169291000,
            'cash': 4037442000,
            'cash_flow_op': 1144641000,
            'cash_flow_inv': -835635000,
            'cash_flow_fin': 50363000
        })

    def test_ebay_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1065088/000106508813000058/ebay-20130331.xml')
        self.assert_item(item, {
            'symbol': 'EBAY',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2013-03-31',
            'revenues': 3748000000,
            'op_income': 800000000,
            'net_income': 677000000,
            'eps_basic': 0.52,
            'eps_diluted': 0.51,
            'dividend': 0.0,
            'assets': 38000000000,
            'cur_assets': 22336000000,
            'cur_liab': 11720000000,
            'equity': 21112000000,
            'cash': 6530000000,
            'cash_flow_op': 937000000,
            'cash_flow_inv': -719000000,
            'cash_flow_fin': -411000000
        })

    def test_ecl_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/31462/000110465912072308/ecl-20120930.xml')
        self.assert_item(item, {
            'symbol': 'ECL',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-30',
            'revenues': 3023300000,
            'op_income': 401200000,
            'net_income': 238000000,
            'eps_basic': 0.81,
            'eps_diluted': 0.8,
            'dividend': 0.2,
            'assets': 16722800000,
            'cur_assets': 4072900000,
            'cur_liab': 2818700000,
            'equity': 6026200000,
            'cash': 324000000,
            'cash_flow_op': 720800000,
            'cash_flow_inv': -414900000,
            'cash_flow_fin': -1815800000
        })

    def test_ed_20130930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/23632/000119312513425393/ed-20130930.xml')
        self.assert_item(item, {
            'symbol': 'ED',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2013,
            'end_date': '2013-09-30',
            'revenues': 3484000000,
            'op_income': 855000000,
            'net_income': 464000000,
            'eps_basic': 1.58,
            'eps_diluted': 1.58,
            'dividend': 0.615,
            'assets': 41964000000,
            'cur_assets': 3704000000,
            'cur_liab': 4373000000,
            'equity': 12166000000,
            'cash': 74000000,
            'cash_flow_op': 1238000000,
            'cash_flow_inv': -1895000000,
            'cash_flow_fin': 337000000
        })

    def test_eqt_20101231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/33213/000110465911009751/eqt-20101231.xml')
        self.assert_item(item, {
            'symbol': 'EQT',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2010,
            'end_date': '2010-12-31',
            'revenues': 1322708000,
            'op_income': 470479000,
            'net_income': 227700000,
            'eps_basic': 1.58,
            'eps_diluted': 1.57,
            'dividend': 0.88,
            'assets': 7098438000,
            'cur_assets': 827940000,
            'cur_liab': 596984000,
            'equity': 3078696000,
            'cash': 0.0,
            'cash_flow_op': 789740000,
            'cash_flow_inv': -1239429000,
            'cash_flow_fin': 449689000
        })

    def test_etr_20121231(self):
        # Large file test (121 MB)
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/7323/000006598413000050/etr-20121231.xml')
        self.assert_item(item, {
            'symbol': 'ETR',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2012,
            'end_date': '2012-12-31',
            'revenues': 10302079000,
            'op_income': 1301181000,
            'net_income': 846673000,
            'eps_basic': 4.77,
            'eps_diluted': 4.76,
            'dividend': 3.32,
            'assets': 43202502000,
            'cur_assets': 3683126000,
            'cur_liab': 4106321000,
            'equity': 9291089000,
            'cash': 532569000,
            'cash_flow_op': 2940285000,
            'cash_flow_inv': -3639797000,
            'cash_flow_fin': 538151000
        })

    def test_exc_20100930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/22606/000119312510234590/exc-20100930.xml')
        self.assert_item(item, {
            'symbol': 'EXC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2010,
            'end_date': '2010-09-30',
            'revenues': 5291000000,
            'op_income': 1366000000,
            'net_income': 845000000,
            'eps_basic': 1.28,
            'eps_diluted': 1.27,
            'dividend': 0.53,
            'assets': 50948000000,
            'cur_assets': 6760000000,
            'cur_liab': 3967000000,
            'equity': 13955000000,
            'cash': 2735000000,
            'cash_flow_op': 4112000000,
            'cash_flow_inv': -2037000000,
            'cash_flow_fin': -1350000000
        })

    def test_fast_20090630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/815556/000119312509154691/fast-20090630.xml')
        self.assert_item(item, {
            'symbol': 'FAST',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2009,
            'end_date': '2009-06-30',
            'revenues': 474894000,
            'op_income': 69938000,
            'net_income': 43538000,
            'eps_basic': 0.29,
            'eps_diluted': 0.29,
            'dividend': 0.0,
            'assets': 1328684000,
            'cur_assets': 988997000,
            'cur_liab': 127950000,
            'equity': 1186845000,
            'cash': 173667000,
            'cash_flow_op': 167552000,
            'cash_flow_inv': -28942000,
            'cash_flow_fin': -51986000
        })

    def test_fast_20090930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/815556/000119312509212481/fast-20090930.xml')
        self.assert_item(item, {
            'symbol': 'FAST',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2009,
            'end_date': '2009-09-30',
            'revenues': 489339000,
            'op_income': 76410000,
            'net_income': 47589000,
            'eps_basic': 0.32,
            'eps_diluted': 0.32,
            'dividend': 0.0,
            'assets': 1337764000,
            'cur_assets': 998090000,
            'cur_liab': 138744000,
            'equity': 1185140000,
            'cash': 193744000,
            'cash_flow_op': 253184000,
            'cash_flow_inv': -41031000,
            'cash_flow_fin': -106943000
        })

    def test_fb_20120630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1326801/000119312512325997/fb-20120630.xml')
        self.assert_item(item, {
            'symbol': 'FB',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2012,
            'end_date': '2012-06-30',
            'revenues': 1184000000,
            'op_income': -743000000,
            'net_income': -157000000,
            'eps_basic': -0.08,
            'eps_diluted': -0.08,
            'dividend': 0.0,
            'assets': 14928000000,
            'cur_assets': 11967000000,
            'cur_liab': 1034000000,
            'equity': 13309000000,
            'cash': 2098000000,
            'cash_flow_op': 683000000,
            'cash_flow_inv': -7170000000,
            'cash_flow_fin': 7090000000
        })

    def test_fb_20121231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1326801/000132680113000003/fb-20121231.xml')
        self.assert_item(item, {
            'symbol': 'FB',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2012,
            'end_date': '2012-12-31',
            'revenues': 5089000000,
            'op_income': 538000000,
            'net_income': 32000000,
            'eps_basic': 0.02,
            'eps_diluted': 0.01,
            'dividend': 0.0,
            'assets': 15103000000,
            'cur_assets': 11267000000,
            'cur_liab': 1052000000,
            'equity': 11755000000,
            'cash': 2384000000,
            'cash_flow_op': 1612000000,
            'cash_flow_inv': -7024000000,
            'cash_flow_fin': 6283000000
        })

    def test_fll_20121231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/891482/000118811213000562/fll-20121231.xml')
        self.assert_item(item, {
            'symbol': 'FLL',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2012,
            'end_date': '2012-12-31',
            'revenues': 128760000,
            'op_income': 49638000,
            'net_income': 27834000,
            'eps_basic': 1.49,
            'eps_diluted': None,
            'dividend': 0.0,
            'assets': 162725000,
            'cur_assets': 32339000,
            'cur_liab': 15332000,
            'equity': 81133000,
            'cash': 20603000,
            'cash_flow_op': -4301000,
            'cash_flow_inv': 45271000,
            'cash_flow_fin': -35074000
        })

    def test_flr_20080930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1124198/000110465908068715/flr-20080930.xml')
        self.assert_item(item, {
            'symbol': 'FLR',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2008,
            'end_date': '2008-09-30',
            'revenues': 5673818000,
            'op_income': None,
            'net_income': 183099000,
            'eps_basic': 1.03,
            'eps_diluted': 1.01,
            'dividend': 0.125,
            'assets': 6605120000,
            'cur_assets': 4808393000,
            'cur_liab': 3228638000,
            'equity': 2741002000,
            'cash': 1514943000,
            'cash_flow_op': 855198000,
            'cash_flow_inv': -295445000,
            'cash_flow_fin': -202011000
        })

    def test_fmc_20090630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/37785/000119312509165435/fmc-20090630.xml')
        self.assert_item(item, {
            'symbol': 'FMC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2009,
            'end_date': '2009-06-30',
            'revenues': 700300000,
            'op_income': 97200000,
            'net_income': 69300000,
            'eps_basic': 0.95,
            'eps_diluted': 0.94,
            'dividend': 0.0,
            'assets': 3028500000,
            'cur_assets': 1423700000,
            'cur_liab': 717200000,
            'equity': 1101200000,
            'cash': 67000000,
            'cash_flow_op': 173900000,
            'cash_flow_inv': -106500000,
            'cash_flow_fin': -33100000
        })

    def test_fpl_20100331(self):
        # FPL was later changed to NEE
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/37634/000075330810000051/fpl-20100331.xml')
        self.assert_item(item, {
            'symbol': 'FPL',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2010-03-31',
            'revenues': 3622000000,
            'op_income': 939000000,
            'net_income': 556000000,
            'eps_basic': 1.36,
            'eps_diluted': 1.36,
            'dividend': 0.5,
            'assets': 50942000000,
            'cur_assets': 5557000000,
            'cur_liab': 7782000000,
            'equity': 13336000000,
            'cash': 1215000000,
            'cash_flow_op': 896000000,
            'cash_flow_inv': -1361000000,
            'cash_flow_fin': 1442000000
        })

    def test_ftr_20110930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/20520/000002052011000066/ftr-20110930.xml')
        self.assert_item(item, {
            'symbol': 'FTR',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2011,
            'end_date': '2011-09-30',
            'revenues': 1290939000,
            'op_income': 180291000,
            'net_income': 19481000,
            'eps_basic': 0.02,
            'eps_diluted': 0.02,
            'dividend': 0.0,
            'assets': 17493767000,
            'cur_assets': 969746000,
            'cur_liab': 1168142000,
            'equity': 4776588000,
            'cash': 205817000,
            'cash_flow_op': 1272654000,
            'cash_flow_inv': -676974000,
            'cash_flow_fin': -641126000
        })

    def test_ge_20121231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/40545/000004054513000036/ge-20121231.xml')
        self.assert_item(item, {
            'symbol': 'GE',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2012,
            'end_date': '2012-12-31',
            'revenues': 147359000000,
            'op_income': 22887000000,
            'net_income': 13641000000,
            'eps_basic': 1.29,
            'eps_diluted': 1.29,
            'dividend': 0.7,
            'assets': 685328000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 128470000000,
            'cash': 77356000000,
            'cash_flow_op': 31331000000,
            'cash_flow_inv': 11302000000,
            'cash_flow_fin': -51074000000
        })

    def test_gis_20121125(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/40704/000119312512508388/gis-20121125.xml')
        self.assert_item(item, {
            'symbol': 'GIS',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2012-11-25',
            'revenues': 4881800000,
            'op_income': 829000000,
            'net_income': 541600000,
            'eps_basic': 0.84,
            'eps_diluted': 0.82,
            'dividend': 0.33,
            'assets': 22952900000,
            'cur_assets': 4565500000,
            'cur_liab': 5736400000,
            'equity': 7440000000,
            'cash': 734900000,
            'cash_flow_op': 1317100000,
            'cash_flow_inv': -1103200000,
            'cash_flow_fin': 33700000
        })

    def test_gmcr_20110625(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/909954/000119312511214253/gmcr-20110630.xml')
        self.assert_item(item, {
            'symbol': 'GMCR',
            'amend': False,  # it's actually amended, but not marked in XML
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2011,
            'end_date': '2011-06-25',
            'revenues': 717210000,
            'op_income': 119310000,
            'net_income': 56348000,
            'eps_basic': 0.38,
            'eps_diluted': 0.37,
            'dividend': 0.0,
            'assets': 2874422000,
            'cur_assets': 844998000,
            'cur_liab': 395706000,
            'equity': 1816646000,
            'cash': 76138000,
            'cash_flow_op': 174708000,
            'cash_flow_inv': -1082070000,
            'cash_flow_fin': 986183000
        })

    def test_goog_20090930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1288776/000119312509222384/goog-20090930.xml')
        self.assert_item(item, {
            'symbol': 'GOOG',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2009,
            'end_date': '2009-09-30',
            'revenues': 5944851000,
            'op_income': 2073718000,
            'net_income': 1638975000,
            'eps_basic': 5.18,
            'eps_diluted': 5.13,
            'dividend': 0.0,
            'assets': 37702845000,
            'cur_assets': 26353544000,
            'cur_liab': 2321774000,
            'equity': 33721753000,
            'cash': 12087115000,
            'cash_flow_op': 6584667000,
            'cash_flow_inv': -3245963000,
            'cash_flow_fin': 74851000
        })

    def test_goog_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1288776/000119312512440217/goog-20120930.xml')
        self.assert_item(item, {
            'symbol': 'GOOG',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-30',
            'revenues': 14101000000,
            'op_income': 2736000000,
            'net_income': 2176000000,
            'eps_basic': 6.64,
            'eps_diluted': 6.53,
            'dividend': 0.0,
            'assets': 89730000000,
            'cur_assets': 56821000000,
            'cur_liab': 14434000000,
            'equity': 68028000000,
            'cash': 16260000000,
            'cash_flow_op': 11950000000,
            'cash_flow_inv': -7542000000,
            'cash_flow_fin': 1921000000
        })

    def test_goog_20121231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1288776/000119312513028362/goog-20121231.xml')
        self.assert_item(item, {
            'symbol': 'GOOG',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2012,
            'end_date': '2012-12-31',
            'revenues': 50175000000,
            'op_income': 12760000000,
            'net_income': 10737000000,
            'eps_basic': 32.81,
            'eps_diluted': 32.31,
            'dividend': 0.0,
            'assets': 93798000000,
            'cur_assets': 60454000000,
            'cur_liab': 14337000000,
            'equity': 71715000000,
            'cash': 14778000000,
            'cash_flow_op': 16619000000,
            'cash_flow_inv': -13056000000,
            'cash_flow_fin': 1229000000
        })

    def test_goog_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1288776/000128877613000055/goog-20130630.xml')
        self.assert_item(item, {
            'symbol': 'GOOG',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-30',
            'revenues': 14105000000,
            'op_income': 3123000000,
            'net_income': 3228000000,
            'eps_basic': 9.71,
            'eps_diluted': 9.54,
            'dividend': 0.0,
            'assets': 101182000000,
            'cur_assets': 66861000000,
            'cur_liab': 15329000000,
            'equity': 78852000000,
            'cash': 16164000000,
            'cash_flow_op': 8338000000,
            'cash_flow_inv': -6244000000,
            'cash_flow_fin': -622000000
        })

    def test_goog_20140630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1288776/000128877614000065/goog-20140630.xml')
        self.assert_item(item, {
            'symbol': 'GOOG/GOOGL',  # Two symbols, see issue #6
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2014,
            'end_date': '2014-06-30',
            'revenues': 15955000000,
            'op_income': 4258000000,
            'net_income': 3422000000,
            'eps_basic': 5.07,
            'eps_diluted': 4.99,
            'dividend': 0.0,
            'assets': 121608000000,
            'cur_assets': 77905000000,
            'cur_liab': 17097000000,
            'equity': 95749000000,
            'cash': 19620000000,
            'cash_flow_op': 10018000000,
            'cash_flow_inv': -8487000000,
            'cash_flow_fin': -640000000
        })

    def test_gs_20090626(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/886982/000095012309029919/gs-20090626.xml')
        self.assert_item(item, {
            'symbol': 'GS',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2009,
            'end_date': '2009-06-26',
            'revenues': 13761000000,
            'op_income': None,
            'net_income': 2718000000,
            'eps_basic': 5.27,
            'eps_diluted': 4.93,
            'dividend': 0.35,
            'assets': 889544000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 62813000000,
            'cash': 22177000000,
            'cash_flow_op': 16020000000,
            'cash_flow_inv': -772000000,
            'cash_flow_fin': -6876000000
        })

    def test_hon_20120331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/773840/000093041312002323/hon-20120331.xml')
        self.assert_item(item, {
            'symbol': 'HON',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2012,
            'end_date': '2012-03-31',
            'revenues': 9307000000,
            'op_income': None,
            'net_income': 823000000,
            'eps_basic': 1.06,
            'eps_diluted': 1.04,
            'dividend': 0.3725,
            'assets': 40370000000,
            'cur_assets': 16553000000,
            'cur_liab': 12666000000,
            'equity': 11842000000,
            'cash': 3988000000,
            'cash_flow_op': 196000000,
            'cash_flow_inv': -122000000,
            'cash_flow_fin': 169000000
        })

    def test_hrb_20090731(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12659/000095012309041361/hrb-20090731.xml')
        self.assert_item(item, {
            'symbol': 'HRB',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2009-07-31',
            'revenues': 275505000,
            'op_income': -214162000,
            'net_income': -133634000,
            'eps_basic': -0.4,
            'eps_diluted': -0.4,
            'dividend': 0.15,
            'assets': 4545762000,
            'cur_assets': 1828146000,
            'cur_liab': 1823126000,
            'equity': 1190714000,
            'cash': 1006303000,
            'cash_flow_op': -454577000,
            'cash_flow_inv': 15360000,
            'cash_flow_fin': -216206000
        })

    def test_hrb_20091031(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12659/000095012309069608/hrb-20091031.xml')
        self.assert_item(item, {
            'symbol': 'HRB',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2010,
            'end_date': '2009-10-31',
            'revenues': 326081000,
            'op_income': -214553000,
            'net_income': -128587000,
            'eps_basic': -0.38,
            'eps_diluted': -0.38,
            'dividend': 0.15,
            'assets': 4967359000,
            'cur_assets': 2300986000,
            'cur_liab': 2382867000,
            'equity': 1071097000,
            'cash': 1432243000,
            'cash_flow_op': -786152000,
            'cash_flow_inv': 43280000,
            'cash_flow_fin': 511231000
        })

    def test_hrb_20130731(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12659/000157484213000013/hrb-20130731.xml')
        self.assert_item(item, {
            'symbol': 'HRB',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2014,
            'end_date': '2013-07-31',
            'revenues': 127195000,
            'op_income': -179555000,
            'net_income': -115187000,
            'eps_basic': -0.42,
            'eps_diluted': -0.42,
            'dividend': 0.20,
            'assets': 3762888000,
            'cur_assets': 1704932000,
            'cur_liab': 1450484000,
            'equity': 1105315000,
            'cash': 1163876000,
            'cash_flow_op': -318742000,
            'cash_flow_inv': -29090000,
            'cash_flow_fin': -229255000
        })

    def test_ihc_20120331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/701869/000070186912000029/ihc-20120331.xml')
        self.assert_item(item, {
            'symbol': 'IHC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2012,
            'end_date': '2012-03-31',
            'revenues': 102156000,
            'op_income': 6416000,
            'net_income': 3922000,
            'eps_basic': 0.22,
            'eps_diluted': 0.22,
            'dividend': 0.0,
            'assets': 1364411000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 280250000,
            'cash': 9286000,
            'cash_flow_op': -138843000,
            'cash_flow_inv': 130710000,
            'cash_flow_fin': -808000
        })

    def test_intc_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/50863/000119312512075534/intc-20111231.xml')
        self.assert_item(item, {
            'symbol': 'INTC',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2011-12-31',
            'revenues': 53999000000,
            'op_income': 17477000000,
            'net_income': 12942000000,
            'eps_basic': 2.46,
            'eps_diluted': 2.39,
            'dividend': 0.7824,
            'assets': 71119000000,
            'cur_assets': 25872000000,
            'cur_liab': 12028000000,
            'equity': 45911000000,
            'cash': 5065000000,
            'cash_flow_op': 20963000000,
            'cash_flow_inv': -10301000000,
            'cash_flow_fin': -11100000000
        })

    def test_intu_20101031(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/896878/000095012310111135/intu-20101031.xml')
        self.assert_item(item, {
            'symbol': 'INTU',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2011,
            'end_date': '2010-10-31',
            'revenues': 532000000,
            'op_income': -104000000,
            'net_income': -70000000,
            'eps_basic': -0.22,
            'eps_diluted': -0.22,
            'dividend': 0.0,
            'assets': 4943000000,
            'cur_assets': 2010000000,
            'cur_liab': 1136000000,
            'equity': 2615000000,
            'cash': 112000000,
            'cash_flow_op': -211000000,
            'cash_flow_inv': 285000000,
            'cash_flow_fin': -177000000
        })

    def test_jnj_20120101(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/200406/000119312512075565/jnj-20120101.xml')
        self.assert_item(item, {
            'symbol': 'JNJ',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2012-01-01',
            'revenues': 65030000000,
            'op_income': 13765000000,
            'net_income': 9672000000,
            'eps_basic': 3.54,
            'eps_diluted': 3.49,
            'dividend': 2.25,
            'assets': 113644000000,
            'cur_assets': 54316000000,
            'cur_liab': 22811000000,
            'equity': 57080000000,
            'cash': 24542000000,
            'cash_flow_op': 14298000000,
            'cash_flow_inv': -4612000000,
            'cash_flow_fin': -4452000000
        })

    def test_jnj_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/200406/000020040612000140/jnj-20120930.xml')
        self.assert_item(item, {
            'symbol': 'JNJ',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-30',
            'revenues': 17052000000,
            'op_income': 3825000000,
            'net_income': 2968000000,
            'eps_basic': 1.08,
            'eps_diluted': 1.05,
            'dividend': 0.61,
            'assets': 118951000000,
            'cur_assets': 44791000000,
            'cur_liab': 23935000000,
            'equity': 63761000000,
            'cash': 15486000000,
            'cash_flow_op': 12020000000,
            'cash_flow_inv': -2007000000,
            'cash_flow_fin': -19091000000
        })

    def test_jnj_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/200406/000020040613000091/jnj-20130630.xml')
        self.assert_item(item, {
            'symbol': 'JNJ',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-30',
            'revenues': 17877000000,
            'op_income': 5020000000,
            'net_income': 3833000000,
            'eps_basic': 1.36,
            'eps_diluted': 1.33,
            'dividend': 0.66,
            'assets': 124325000000,
            'cur_assets': 51273000000,
            'cur_liab': 23767000000,
            'equity': 69665000000,
            'cash': 17307000000,
            'cash_flow_op': 7328000000,
            'cash_flow_inv': -1972000000,
            'cash_flow_fin': -2754000000
        })

    def test_jpm_20090630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/19617/000095012309032832/jpm-20090630.xml')
        self.assert_item(item, {
            'symbol': 'JPM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2009,
            'end_date': '2009-06-30',
            'revenues': 25623000000,
            'op_income': None,
            'net_income': 1072000000,
            'eps_basic': 0.28,
            'eps_diluted': 0.28,
            'dividend': 0.05,
            'assets': 2026642000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 154766000000,
            'cash': 25133000000,
            'cash_flow_op': 103259000000,
            'cash_flow_inv': 34430000000,
            'cash_flow_fin': -139413000000
        })

    def test_jpm_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/19617/000001961712000163/jpm-20111231.xml')
        self.assert_item(item, {
            'symbol': 'JPM',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2011-12-31',
            'revenues': 97234000000,
            'op_income': None,
            'net_income': 17568000000,
            'eps_basic': 4.50,
            'eps_diluted': 4.48,
            'dividend': 1.0,
            'assets': 2265792000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 183573000000,
            'cash': 59602000000,
            'cash_flow_op': 95932000000,
            'cash_flow_inv': -170752000000,
            'cash_flow_fin': 107706000000
        })

    def test_jpm_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/19617/000001961713000300/jpm-20130331.xml')
        self.assert_item(item, {
            'symbol': 'JPM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2013-03-31',
            'revenues': 25122000000,
            'op_income': None,
            'net_income': 6131000000,
            'eps_basic': 1.61,
            'eps_diluted': 1.59,
            'dividend': 0.30,
            'assets': 2389349000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 207086000000,
            'cash': 45524000000,
            'cash_flow_op': 19964000000,
            'cash_flow_inv': -55455000000,
            'cash_flow_fin': 28180000000
        })

    def test_ko_20100402(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/21344/000104746910004416/ko-20100402.xml')
        self.assert_item(item, {
            'symbol': 'KO',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2010-04-02',
            'revenues': 7525000000,
            'op_income': 2183000000,
            'net_income': 1614000000,
            'eps_basic': 0.70,
            'eps_diluted': 0.69,
            'dividend': 0.44,
            'assets': 47403000000,
            'cur_assets': 17208000000,
            'cur_liab': 13583000000,
            'equity': 25157000000,
            'cash': 5684000000,
            'cash_flow_op': 1326000000,
            'cash_flow_inv': -1368000000,
            'cash_flow_fin': -1043000000
        })

    def test_ko_20101231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/21344/000104746911001506/ko-20101231.xml')
        self.assert_item(item, {
            'symbol': 'KO',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2010,
            'end_date': '2010-12-31',
            'revenues': 35119000000,
            'op_income': 8449000000,
            'net_income': 11809000000,
            'eps_basic': 5.12,
            'eps_diluted': 5.06,
            'dividend': 1.76,
            'assets': 72921000000,
            'cur_assets': 21579000000,
            'cur_liab': 18508000000,
            'equity': 31317000000,
            'cash': 8517000000,
            'cash_flow_op': 9532000000,
            'cash_flow_inv': -4405000000,
            'cash_flow_fin': -3465000000
        })

    def test_ko_20120928(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/21344/000002134412000051/ko-20120928.xml')
        self.assert_item(item, {
            'symbol': 'KO',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-28',
            'revenues': 12340000000,
            'op_income': 2793000000,
            'net_income': 2311000000,
            'eps_basic': 0.51,
            'eps_diluted': 0.50,
            'dividend': 0.255,
            'assets': 86654000000,
            'cur_assets': 29712000000,
            'cur_liab': 27008000000,
            'equity': 33590000000,
            'cash': 9615000000,
            'cash_flow_op': 7840000000,
            'cash_flow_inv': -10399000000,
            'cash_flow_fin': -399000000
        })

    def test_krft_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1545158/000119312512495570/krft-20120930.xml')
        self.assert_item(item, {
            'symbol': 'KRFT',
            'amend': True,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-30',
            'revenues': 4606000000,
            'op_income': 762000000,
            'net_income': 470000000,
            'eps_basic': 0.79,
            'eps_diluted': 0.79,
            'dividend': 0.0,
            'assets': 22284000000,
            'cur_assets': 3905000000,
            'cur_liab': 2569000000,
            'equity': 7458000000,
            'cash': 244000000,
            'cash_flow_op': 2067000000,
            'cash_flow_inv': -279000000,
            'cash_flow_fin': -1548000000
        })

    def test_l_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/60086/000119312510105707/l-20100331.xml')
        self.assert_item(item, {
            'symbol': 'L',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2010-03-31',
            'revenues': 3713000000,
            'op_income': None,
            'net_income': 420000000,
            'eps_basic': 0.99,
            'eps_diluted': 0.99,
            'dividend': 0.0625,
            'assets': 75855000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 21993000000,
            'cash': 135000000,
            'cash_flow_op': 294000000,
            'cash_flow_inv': -411000000,
            'cash_flow_fin': 64000000
        })

    def test_l_20100930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/60086/000119312510245478/l-20100930.xml')
        self.assert_item(item, {
            'symbol': 'L',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2010,
            'end_date': '2010-09-30',
            'revenues': 3701000000,
            'op_income': None,
            'net_income': 36000000,
            'eps_basic': 0.09,
            'eps_diluted': 0.09,
            'dividend': 0.0625,
            'assets': 76821000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 23499000000,
            'cash': 132000000,
            'cash_flow_op': 895000000,
            'cash_flow_inv': -426000000,
            'cash_flow_fin': -527000000
        })

    def test_lbtya_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1316631/000119312510111069/lbtya-20100331.xml')
        self.assert_item(item, {
            'symbol': 'LBTYA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2010-03-31',
            'revenues': 2178900000,
            'op_income': 303600000,
            'net_income': 736600000,
            'eps_basic': 2.75,
            'eps_diluted': 2.75,
            'dividend': 0.0,
            'assets': 33083500000,
            'cur_assets': 5524900000,
            'cur_liab': 4107000000,
            'equity': 4066000000,
            'cash': 4184200000,
            'cash_flow_op': 803300000,
            'cash_flow_inv': 45400000,
            'cash_flow_fin': 170700000
        })

    def test_lcapa_20110930(self):
        # This symbol was changed to STRZA
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1507934/000150793411000006/lcapa-20110930.xml')
        self.assert_item(item, {
            'symbol': 'LCAPA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2011,
            'end_date': '2011-09-30',
            'revenues': 540000000,
            'op_income': 111000000,
            'net_income': -42000000,
            'eps_basic': -0.07,
            'eps_diluted': -0.12,
            'dividend': 0.0,
            'assets': 8915000000,
            'cur_assets': 3767000000,
            'cur_liab': 3012000000,
            'equity': 5078000000,
            'cash': 1937000000,
            'cash_flow_op': 316000000,
            'cash_flow_inv': -205000000,
            'cash_flow_fin': -264000000
        })

    def test_linta_20120331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1355096/000135509612000008/linta-20120331.xml')
        self.assert_item(item, {
            'symbol': 'LINTA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2012,
            'end_date': '2012-03-31',
            'revenues': 2314000000,
            'op_income': 258000000,
            'net_income': 91000000,
            'eps_basic': 0.16,
            'eps_diluted': 0.16,
            'dividend': 0.0,
            'assets': 17144000000,
            'cur_assets': 2764000000,
            'cur_liab': 3486000000,
            'equity': 6505000000,
            'cash': 794000000,
            'cash_flow_op': 330000000,
            'cash_flow_inv': -91000000,
            'cash_flow_fin': -284000000
        })

    def test_lll_20100625(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1039101/000095012310071159/lll-20100625.xml')
        self.assert_item(item, {
            'symbol': 'LLL',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2010,
            'end_date': '2010-06-25',
            'revenues': -3966000000,  # a doc's error, should be 3966M
            'op_income': -442000000,  # a doc's error, should be 442M
            'net_income': -228000000,  # a doc's error, should be 227M
            'eps_basic': 1.97,
            'eps_diluted': 1.95,
            'dividend': 0.4,
            'assets': 15689000000,
            'cur_assets': 5494000000,
            'cur_liab': 3730000000,
            'equity': 6926000000,
            'cash': 1023000000,
            'cash_flow_op': 589000000,
            'cash_flow_inv': -688000000,
            'cash_flow_fin': 132000000
        })

    def test_lltc_20110102(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/791907/000079190711000016/lltc-20110102.xml')
        self.assert_item(item, {
            'symbol': 'LLTC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2011,
            'end_date': '2011-01-02',
            'revenues': 383621000,
            'op_income': 201059000,
            'net_income': 143743000,
            'eps_basic': 0.62,
            'eps_diluted': 0.62,
            'dividend': 0.23,
            'assets': 1446186000,
            'cur_assets': 1069958000,
            'cur_liab': 199210000,
            'equity': 278793000,
            'cash': 203308000,
            'cash_flow_op': 342333000,
            'cash_flow_inv': 39771000,
            'cash_flow_fin': -474650000
        })

    def test_lltc_20111002(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/791907/000079190711000080/lltc-20111007.xml')
        self.assert_item(item, {
            'symbol': 'LLTC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2012,
            'end_date': '2011-10-02',
            'revenues': 329920000,
            'op_income': 157566000,
            'net_income': 108401000,
            'eps_basic': 0.47,
            'eps_diluted': 0.47,
            'dividend': 0.24,
            'assets': 1659341000,
            'cur_assets': 1268413000,
            'cur_liab': 169006000,
            'equity': 543199000,
            'cash': 163414000,
            'cash_flow_op': 149860000,
            'cash_flow_inv': -171884000,
            'cash_flow_fin': -85085000
        })

    def test_lly_20100930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/59478/000095012310097867/lly-20100930.xml')
        self.assert_item(item, {
            'symbol': 'LLY',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2010,
            'end_date': '2010-09-30',
            'revenues': 5654800000,
            'op_income': None,
            'net_income': 1302900000,
            'eps_basic': 1.18,
            'eps_diluted': 1.18,
            'dividend': 0.49,
            'assets': 29904300000,
            'cur_assets': 14184300000,
            'cur_liab': 6097400000,
            'equity': 12405500000,
            'cash': 5908800000,
            'cash_flow_op': 4628700000,
            'cash_flow_inv': -1595300000,
            'cash_flow_fin': -1472300000
        })

    def test_lmca_20120331(self):
        # This symbol was changed to STRZA
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1507934/000150793412000012/lmca-20120331.xml')
        self.assert_item(item, {
            'symbol': 'LMCA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2012,
            'end_date': '2012-03-31',
            'revenues': 440000000,
            'op_income': 89000000,
            'net_income': 137000000,
            'eps_basic': 1.13,
            'eps_diluted': 1.10,
            'dividend': 0.0,
            'assets': 7122000000,
            'cur_assets': 3380000000,
            'cur_liab': 547000000,
            'equity': 5321000000,
            'cash': 1915000000,
            'cash_flow_op': 94000000,
            'cash_flow_inv': 581000000,
            'cash_flow_fin': -830000000
        })

    def test_lnc_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/59558/000005955812000143/lnc-20120930.xml')
        self.assert_item(item, {
            'symbol': 'LNC',
            'amend': False,  # mistake in doc, should be True
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-30',
            'revenues': None,  # missing in doc, should be 2954000000
            'op_income': None,
            'net_income': 402000000,
            'eps_basic': 1.45,
            'eps_diluted': 1.41,
            'dividend': 0.0,
            'assets': 215458000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 15237000000,
            'cash': 4373000000,
            'cash_flow_op': 666000000,
            'cash_flow_inv': -2067000000,
            'cash_flow_fin': 1264000000
        })

    def test_ltd_20111029(self):
        # This symbol was changed to LB
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/701985/000144530511003514/ltd-20111029.xml')
        self.assert_item(item, {
            'symbol': 'LTD',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2011,
            'end_date': '2011-10-29',
            'revenues': 2174000000,
            'op_income': 186000000,
            'net_income': 94000000,
            'eps_basic': 0.32,
            'eps_diluted': 0.31,
            'dividend': 0.2,
            'assets': 6517000000,
            'cur_assets': 2616000000,
            'cur_liab': 1504000000,
            'equity': 521000000,
            'cash': 498000000,
            'cash_flow_op': 94000000,
            'cash_flow_inv': -239000000,
            'cash_flow_fin': -489000000
        })

    def test_ltd_20130803(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/701985/000070198513000032/ltd-20130803.xml')
        self.assert_item(item, {
            'symbol': 'LTD',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-08-03',
            'revenues': 2516000000,
            'op_income': 358000000,
            'net_income': 178000000,
            'eps_basic': 0.62,
            'eps_diluted': 0.61,
            'dividend': 0.3,
            'assets': 6072000000,
            'cur_assets': 2098000000,
            'cur_liab': 1485000000,
            'equity': -861000000,
            'cash': 551000000,
            'cash_flow_op': 354000000,
            'cash_flow_inv': -381000000,
            'cash_flow_fin': -194000000
        })

    def test_luv_20110630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/92380/000009238011000070/luv-20110630.xml')
        self.assert_item(item, {
            'symbol': 'LUV',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2011,
            'end_date': '2011-06-30',
            'revenues': 4136000000,
            'op_income': 207000000,
            'net_income': 161000000,
            'eps_basic': 0.21,
            'eps_diluted': 0.21,
            'dividend': 0.0045,
            'assets': 18945000000,
            'cur_assets': 5421000000,
            'cur_liab': 5318000000,
            'equity': 7202000000,
            'cash': 1595000000,
            'cash_flow_op': 237000000,
            'cash_flow_inv': -589000000,
            'cash_flow_fin': -92000000
        })

    def test_mchp_20120630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/827054/000082705412000230/mchp-20120630.xml')
        self.assert_item(item, {
            'symbol': 'MCHP',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2012-06-30',
            'revenues': 352134000,
            'op_income': 96333000,
            'net_income': 78710000,
            'eps_basic': 0.41,
            'eps_diluted': 0.39,
            'dividend': 0.35,
            'assets': 3144840000,
            'cur_assets': 2229298000,
            'cur_liab': 249989000,
            'equity': 2017990000,
            'cash': 779848000,
            'cash_flow_op': 128971000,
            'cash_flow_inv': 77890000,
            'cash_flow_fin': -62768000
        })

    def test_mdlz_20130930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1103982/000119312513431957/mdlz-20130930.xml')
        self.assert_item(item, {
            'symbol': 'MDLZ',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2013,
            'end_date': '2013-09-30',
            'revenues': 8472000000,
            'op_income': 1262000000,
            'net_income': 1024000000,
            'eps_basic': 0.58,
            'eps_diluted': 0.57,
            'dividend': 0.14,
            'assets': 74859000000,
            'cur_assets': 15463000000,
            'cur_liab': 15269000000,
            'equity': 32492000000,
            'cash': 3692000000,
            'cash_flow_op': 1198000000,
            'cash_flow_inv': -1015000000,
            'cash_flow_fin': -881000000
        })

    def test_mmm_20091231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/66740/000110465910007295/mmm-20091231.xml')
        self.assert_item(item, {
            'symbol': 'MMM',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2009,
            'end_date': '2009-12-31',
            'revenues': 23123000000,
            'op_income': 4814000000,
            'net_income': 3193000000,
            'eps_basic': 4.56,
            'eps_diluted': 4.52,
            'dividend': 2.04,
            'assets': 27250000000,
            'cur_assets': 10795000000,
            'cur_liab': 4897000000,
            'equity': 13302000000,
            'cash': 3040000000,
            'cash_flow_op': 4941000000,
            'cash_flow_inv': -1732000000,
            'cash_flow_fin': -2014000000
        })

    def test_mmm_20120331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/66740/000110465912032441/mmm-20120331.xml')
        self.assert_item(item, {
            'symbol': 'MMM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2012,
            'end_date': '2012-03-31',
            'revenues': 7486000000,
            'op_income': 1634000000,
            'net_income': 1125000000,
            'eps_basic': 1.61,
            'eps_diluted': 1.59,
            'dividend': 0.59,
            'assets': 32015000000,
            'cur_assets': 12853000000,
            'cur_liab': 5408000000,
            'equity': 16619000000,
            'cash': 2332000000,
            'cash_flow_op': 828000000,
            'cash_flow_inv': -43000000,
            'cash_flow_fin': -722000000
        })

    def test_mmm_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/66740/000110465913058961/mmm-20130630.xml')
        self.assert_item(item, {
            'symbol': 'MMM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-30',
            'revenues': 7752000000,
            'op_income': 1702000000,
            'net_income': 1197000000,
            'eps_basic': 1.74,
            'eps_diluted': 1.71,
            'dividend': 0.635,
            'assets': 34130000000,
            'cur_assets': 13983000000,
            'cur_liab': 6335000000,
            'equity': 18319000000,
            'cash': 2942000000,
            'cash_flow_op': 2673000000,
            'cash_flow_inv': -740000000,
            'cash_flow_fin': -1727000000
        })

    def test_mnst_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/865752/000110465913062263/mnst-20130630.xml')
        self.assert_item(item, {
            'symbol': 'MNST',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-30',
            'revenues': 630934000,
            'op_income': 179427000,
            'net_income': 106873000,
            'eps_basic': 0.64,
            'eps_diluted': 0.62,
            'dividend': 0.0,
            'assets': 1317842000,
            'cur_assets': 1093822000,
            'cur_liab': 346174000,
            'equity': 856021000,
            'cash': 283839000,
            'cash_flow_op': 99720000,
            'cash_flow_inv': -70580000,
            'cash_flow_fin': 30981000
        })

    def test_msft_20110630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/789019/000119312511200680/msft-20110630.xml')
        self.assert_item(item, {
            'symbol': 'MSFT',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2011-06-30',
            'revenues': 69943000000,
            'op_income': 27161000000,
            'net_income': 23150000000,
            'eps_basic': 2.73,
            'eps_diluted': 2.69,
            'dividend': 0.64,
            'assets': 108704000000,
            'cur_assets': 74918000000,
            'cur_liab': 28774000000,
            'equity': 57083000000,
            'cash': 9610000000,
            'cash_flow_op': 26994000000,
            'cash_flow_inv': -14616000000,
            'cash_flow_fin': -8376000000
        })

    def test_msft_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/789019/000119312512026864/msft-20111231.xml')
        self.assert_item(item, {
            'symbol': 'MSFT',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2012,
            'end_date': '2011-12-31',
            'revenues': 20885000000,
            'op_income': 7994000000,
            'net_income': 6624000000,
            'eps_basic': 0.79,
            'eps_diluted': 0.78,
            'dividend': 0.20,
            'assets': 112243000000,
            'cur_assets': 72513000000,
            'cur_liab': 25373000000,
            'equity': 64121000000,
            'cash': 10610000000,
            'cash_flow_op': 5862000000,
            'cash_flow_inv': -5568000000,
            'cash_flow_fin': -2513000000
        })

    def test_msft_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/789019/000119312513160748/msft-20130331.xml')
        self.assert_item(item, {
            'symbol': 'MSFT',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2013,
            'end_date': '2013-03-31',
            'revenues': 20489000000,
            'op_income': 7612000000,
            'net_income': 6055000000,
            'eps_basic': 0.72,
            'eps_diluted': 0.72,
            'dividend': 0.23,
            'assets': 134105000000,
            'cur_assets': 93524000000,
            'cur_liab': 31929000000,
            'equity': 76688000000,
            'cash': 5240000000,
            'cash_flow_op': 9666000000,
            'cash_flow_inv': -7660000000,
            'cash_flow_fin': -2744000000
        })

    def test_mu_20121129(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/723125/000072312513000007/mu-20121129.xml')
        self.assert_item(item, {
            'symbol': 'MU',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2012-11-29',
            'revenues': 1834000000,
            'op_income': -157000000,
            'net_income': -275000000,
            'eps_basic': -0.27,
            'eps_diluted': -0.27,
            'dividend': 0.0,
            'assets': 14067000000,
            'cur_assets': 5315000000,
            'cur_liab': 2138000000,
            'equity': 8186000000,
            'cash': 2102000000,
            'cash_flow_op': 236000000,
            'cash_flow_inv': -639000000,
            'cash_flow_fin': 46000000
        })

    def test_mxim_20110326(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/743316/000144530511000751/mxim-20110422.xml')
        self.assert_item(item, {
            'symbol': 'MXIM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2011,
            'end_date': '2011-03-26',
            'revenues': 606775000,
            'op_income': 163995000,
            'net_income': 136276000,
            'eps_basic': 0.46,
            'eps_diluted': 0.45,
            'dividend': 0.21,
            'assets': 3452417000,
            'cur_assets': 1676593000,
            'cur_liab': 391153000,
            'equity': 2465040000,
            'cash': 868923000,
            'cash_flow_op': 615180000,
            'cash_flow_inv': -224755000,
            'cash_flow_fin': -348014000
        })

    def test_nflx_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1065280/000106528012000020/nflx-20120930.xml')
        self.assert_item(item, {
            'symbol': 'NFLX',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-30',
            'revenues': 905089000,
            'op_income': 16135000,
            'net_income': 7675000,
            'eps_basic': 0.14,
            'eps_diluted': 0.13,
            'dividend': 0.0,
            'assets': 3808833000,
            'cur_assets': 2225018000,
            'cur_liab': 1598223000,
            'equity': 716840000,
            'cash': 370298000,
            'cash_flow_op': 150000,
            'cash_flow_inv': -33524000,
            'cash_flow_fin': -158000
        })

    def test_nvda_20130127(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1045810/000104581013000008/nvda-20130127.xml')
        self.assert_item(item, {
            'symbol': 'NVDA',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2013,
            'end_date': '2013-01-27',
            'revenues': 4280159000,
            'op_income': 648239000,
            'net_income': 562536000,
            'eps_basic': 0.91,
            'eps_diluted': 0.9,
            'dividend': 0.075,
            'assets': 6412245000,
            'cur_assets': 4775258000,
            'cur_liab': 976223000,
            'equity': 4827703000,
            'cash': 732786000,
            'cash_flow_op': 824172000,
            'cash_flow_inv': -743992000,
            'cash_flow_fin': -15270000
        })

    def test_nws_20090930(self):
        # This symbol was changed to FOX
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1308161/000119312509224062/nws-20090930.xml')
        self.assert_item(item, {
            'symbol': 'NWS',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2009-09-30',
            'revenues': 7199000000,
            'op_income': 1042000000,
            'net_income': 571000000,
            'eps_basic': 0.22,
            'eps_diluted': 0.22,
            'dividend': 0.06,
            'assets': 55316000000,
            'cur_assets': 17425000000,
            'cur_liab': 10990000000,
            'equity': 24479000000,
            'cash': 7832000000,
            'cash_flow_op': 680000000,
            'cash_flow_inv': -362000000,
            'cash_flow_fin': 942000000
        })

    def test_omx_20110924(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12978/000119312511286448/omx-20110924.xml')
        self.assert_item(item, {
            'symbol': 'OMX',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2011,
            'end_date': '2011-09-24',
            'revenues': 1774767000,
            'op_income': 41296000,
            'net_income': 21518000,
            'eps_basic': 0.25,
            'eps_diluted': 0.25,
            'dividend': 0.0,
            'assets': 4002981000,
            'cur_assets': 1950996000,
            'cur_liab': 998377000,
            'equity': 657636000,
            'cash': 485426000,
            'cash_flow_op': 78743000,
            'cash_flow_inv': -41380000,
            'cash_flow_fin': -11280000
        })

    def test_omx_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12978/000119312512077611/omx-20111231.xml')
        self.assert_item(item, {
            'symbol': 'OMX',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2011-12-31',
            'revenues': 7121167000,
            'op_income': 86486000,
            'net_income': 32771000,
            'eps_basic': 0.38,
            'eps_diluted': 0.38,
            'dividend': 0.0,
            'assets': 4069275000,
            'cur_assets': 1938974000,
            'cur_liab': 1013301000,
            'equity': 568993000,
            'cash': 427111000,
            'cash_flow_op': 53679000,
            'cash_flow_inv': -69373000,
            'cash_flow_fin': -17952000
        })

    def test_omx_20121229(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12978/000119312513073972/omx-20121229.xml')
        self.assert_item(item, {
            'symbol': 'OMX',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2012,
            'end_date': '2012-12-29',
            'revenues': 6920384000,
            'op_income': 24278000,
            'net_income': 414694000,
            'eps_basic': 4.79,
            'eps_diluted': 4.74,
            'dividend': 0.0,
            'assets': 3784315000,
            'cur_assets': 1983884000,
            'cur_liab': 1056641000,
            'equity': 1034373000,
            'cash': 495056000,
            'cash_flow_op': 185201000,
            'cash_flow_inv': -85244000,
            'cash_flow_fin': -34836000
        })

    def test_orly_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/898173/000089817313000028/orly-20130331.xml')
        self.assert_item(item, {
            'symbol': 'ORLY',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2013-03-31',
            'revenues': 1585009000,
            'op_income': 251084000,
            'net_income': 154329000,
            'eps_basic': 1.38,
            'eps_diluted': 1.36,
            'dividend': 0.0,
            'assets': 5789541000,
            'cur_assets': 2741188000,
            'cur_liab': 2349022000,
            'equity': 2072525000,
            'cash': 205410000,
            'cash_flow_op': 226344000,
            'cash_flow_inv': -72100000,
            'cash_flow_fin': -196962000
        })

    def test_pay_20110430(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1312073/000119312511161119/pay-20110430.xml')
        self.assert_item(item, {
            'symbol': 'PAY',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2011,
            'end_date': '2011-04-30',
            'revenues': 292446000,
            'op_income': 37338000,
            'net_income': 25200000,
            'eps_basic': 0.29,
            'eps_diluted': 0.27,
            'dividend': 0.0,
            'assets': 1252289000,
            'cur_assets': 935395000,
            'cur_liab': 303590000,
            'equity': 332172000,
            'cash': 531542000,
            'cash_flow_op': 68831000,
            'cash_flow_inv': -20049000,
            'cash_flow_fin': 34676000
        })

    def test_pcar_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/75362/000119312510108284/pcar-20100331.xml')
        self.assert_item(item, {
            'symbol': 'PCAR',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2010-03-31',
            'revenues': 2230700000,
            'op_income': None,
            'net_income': 68300000,
            'eps_basic': 0.19,
            'eps_diluted': 0.19,
            'dividend': 0.09,
            'assets': 13990000000,
            'cur_assets': 3396400000,
            'cur_liab': 1425900000,
            'equity': 5092600000,
            'cash': 1854700000,
            'cash_flow_op': 285400000,
            'cash_flow_inv': 40500000,
            'cash_flow_fin': -350800000
        })

    def test_pcg_20091231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1004980/000100498010000015/pcg-20091231.xml')
        self.assert_item(item, {
            'symbol': 'PCG',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2009,
            'end_date': '2009-12-31',
            'revenues': 13399000000,
            'op_income': 2299000000,
            'net_income': 1220000000,
            'eps_basic': 3.25,
            'eps_diluted': 3.2,
            'dividend': 1.68,
            'assets': 42945000000,
            'cur_assets': 5657000000,
            'cur_liab': 6813000000,
            'equity': 10585000000,
            'cash': 527000000,
            'cash_flow_op': 3039000000,
            'cash_flow_inv': -3336000000,
            'cash_flow_fin': 605000000
        })

    def test_plt_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/914025/000091402513000049/plt-20130630.xml')
        self.assert_item(item, {
            'symbol': 'PLT',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2014,
            'end_date': '2013-06-30',
            'revenues': 202818000,
            'op_income': 35949000,
            'net_income': 26953000,
            'eps_basic': 0.63,
            'eps_diluted': 0.62,
            'dividend': 0.1,
            'assets': 780520000,
            'cur_assets': 568272000,
            'cur_liab': 90121000,
            'equity': 673569000,
            'cash': 256343000,
            'cash_flow_op': 34140000,
            'cash_flow_inv': -4120000,
            'cash_flow_fin': -2424000
        })

    def test_qep_20110630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1108827/000119312511202252/qep-20110630.xml')
        self.assert_item(item, {
            'symbol': 'QEP',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2011,
            'end_date': '2011-06-30',
            'revenues': 784100000,
            'op_income': 168900000,
            'net_income': 92800000,
            'eps_basic': 0.52,
            'eps_diluted': 0.52,
            'dividend': 0.02,
            'assets': 7075000000,
            'cur_assets': 655600000,
            'cur_liab': 582900000,
            'equity': 3184400000,
            'cash': None,
            'cash_flow_op': 628600000,
            'cash_flow_inv': -660200000,
            'cash_flow_fin': 31600000
        })

    def test_qep_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1108827/000110882712000006/qep-20120930.xml')
        self.assert_item(item, {
            'symbol': 'QEP',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-30',
            'revenues': 542400000,
            'op_income': -12600000,
            'net_income': -3100000,
            'eps_basic': -0.02,
            'eps_diluted': -0.02,
            'dividend': 0.02,
            'assets': 8996100000,
            'cur_assets': 619800000,
            'cur_liab': 616700000,
            'equity': 3377000000,
            'cash': 0.0,
            'cash_flow_op': 972000000,
            'cash_flow_inv': -2435700000,
            'cash_flow_fin': 1463700000
        })

    def test_regn_20100630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/872589/000120677410001689/regn-20100630.xml')
        self.assert_item(item, {
            'symbol': 'REGN',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2010,
            'end_date': '2010-06-30',
            'revenues': 115886000,
            'op_income': -23724000,
            'net_income': -25474000,
            'eps_basic': -0.31,
            'eps_diluted': -0.31,
            'dividend': 0.0,
            'assets': 790641000,
            'cur_assets': 417750000,
            'cur_liab': 119571000,
            'equity': 371216000,
            'cash': 112000000,
            'cash_flow_op': -22626000,
            'cash_flow_inv': -131383000,
            'cash_flow_fin': 58934000
        })

    def test_sbac_20110331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1034054/000119312511130220/sbac-20110331.xml')
        self.assert_item(item, {
            'symbol': 'SBAC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2011,
            'end_date': '2011-03-31',
            'revenues': 167749000,
            'op_income': 23899000,
            'net_income': -34251000,
            'eps_basic': -0.3,
            'eps_diluted': -0.3,
            'dividend': 0.0,
            'assets': 3466258000,
            'cur_assets': 173387000,
            'cur_liab': 120247000,
            'equity': 213078000,
            'cash': 95104000,
            'cash_flow_op': 53197000,
            'cash_flow_inv': -108748000,
            'cash_flow_fin': 86401000
        })

    def test_shld_20101030(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1310067/000119312510263486/shld-20101030.xml')
        self.assert_item(item, {
            'symbol': 'SHLD',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2010,
            'end_date': '2010-10-30',
            'revenues': 9678000000,
            'op_income': -292000000,
            'net_income': -218000000,
            'eps_basic': -1.98,
            'eps_diluted': -1.98,
            'dividend': 0.0,
            'assets': 26045000000,
            'cur_assets': 13123000000,
            'cur_liab': 10682000000,
            'equity': 8378000000,
            'cash': 790000000,
            'cash_flow_op': -1172000000,
            'cash_flow_inv': -296000000,
            'cash_flow_fin': 532000000
        })

    def test_sial_20101231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/90185/000119312511028579/sial-20101231.xml')
        self.assert_item(item, {
            'symbol': 'SIAL',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2010,
            'end_date': '2010-12-31',
            'revenues': 2271000000,
            'op_income': 551000000,
            'net_income': 384000000,
            'eps_basic': 3.17,
            'eps_diluted': 3.12,
            'dividend': 0.0,
            'assets': 3014000000,
            'cur_assets': 1602000000,
            'cur_liab': 530000000,
            'equity': 1976000000,
            'cash': 569000000,
            'cash_flow_op': 523000000,
            'cash_flow_inv': -182000000,
            'cash_flow_fin': -161000000
        })

    def test_siri_20100630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/908937/000095012310074081/siri-20100630.xml')
        self.assert_item(item, {
            'symbol': 'SIRI',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2010,
            'end_date': '2010-06-30',
            'revenues': 699761000,
            'op_income': 125634000,
            'net_income': 15272000,
            'eps_basic': 0.0,
            'eps_diluted': 0.0,
            'dividend': 0.0,
            'assets': 7200932000,
            'cur_assets': 760172000,
            'cur_liab': 2041871000,
            'equity': 180428000,
            'cash': 258854000,
            'cash_flow_op': 140987000,
            'cash_flow_inv': -159859000,
            'cash_flow_fin': -105763000
        })

    def test_siri_20120331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/908937/000090893712000003/siri-20120331.xml')
        self.assert_item(item, {
            'symbol': 'SIRI',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2012,
            'end_date': '2012-03-31',
            'revenues': 804722000,
            'op_income': 199238000,
            'net_income': 107774000,
            'eps_basic': 0.03,
            'eps_diluted': 0.02,
            'dividend': 0.0,
            'assets': 7501724000,
            'cur_assets': 1337094000,
            'cur_liab': 2236580000,
            'equity': 849579000,
            'cash': 746576000,
            'cash_flow_op': 39948000,
            'cash_flow_inv': -25187000,
            'cash_flow_fin': -42175000
        })

    def test_spex_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/12239/000141588913001019/spex-20130331.xml')
        self.assert_item(item, {
            'symbol': 'SPEX',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2013-03-31',
            'revenues': 5761,
            'op_income': -910547,
            'net_income': -3696570,
            'eps_basic': -5.35,
            'eps_diluted': None,
            'dividend': 0.0,
            'assets': 3572989,
            'cur_assets': 3535555,
            'cur_liab': 453858,
            'equity': 2857993,
            'cash': 3448526,
            'cash_flow_op': -1049711,
            'cash_flow_inv': None,
            'cash_flow_fin': None
        })

    def test_strza_20121231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1507934/000150793413000015/strza-20121231.xml')
        self.assert_item(item, {
            'symbol': 'STRZA',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2012,
            'end_date': '2012-12-31',
            'revenues': 1630696000,
            'op_income': 405404000,
            'net_income': 254484000,
            'eps_basic': None,
            'eps_diluted': None,
            'dividend': 0.0,
            'assets': 2176050000,
            'cur_assets': 1376911000,
            'cur_liab': 330451000,
            'equity': 1302144000,
            'cash': 749774000,
            'cash_flow_op': 292077000,
            'cash_flow_inv': -16214000,
            'cash_flow_fin': -626101000
        })

    def test_stx_20120928(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1137789/000110465912072744/stx-20120928.xml')
        self.assert_item(item, {
            'symbol': 'STX',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2012-09-28',
            'revenues': 3732000000,
            'op_income': 624000000,
            'net_income': 582000000,
            'eps_basic': 1.48,
            'eps_diluted': 1.42,
            'dividend': 0.32,
            'assets': 9522000000,
            'cur_assets': 5749000000,
            'cur_liab': 2753000000,
            'equity': 3535000000,
            'cash': 1894000000,
            'cash_flow_op': 1132000000,
            'cash_flow_inv': -265000000,
            'cash_flow_fin': -681000000
        })

    def test_stx_20121228(self):
        # 'stx-20120928' is misnamed
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1137789/000110465913005497/stx-20120928.xml')
        self.assert_item(item, {
            'symbol': 'STX',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2012-12-28',
            'revenues': 3668000000,
            'op_income': 555000000,
            'net_income': 492000000,
            'eps_basic': 1.33,
            'eps_diluted': 1.3,
            'dividend': 0.7,
            'assets': 8742000000,
            'cur_assets': 5017000000,
            'cur_liab': 2643000000,
            'equity': 2925000000,
            'cash': 1383000000,
            'cash_flow_op': 1976000000,
            'cash_flow_inv': -453000000,
            'cash_flow_fin': -1849000000
        })

    def test_symc_20130628(self):
        # 'symc-20140628.xml' is misnamed
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/849399/000119312513312695/symc-20140628.xml')
        self.assert_item(item, {
            'symbol': 'SYMC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2014,
            'end_date': '2013-06-28',
            'revenues': 1709000000,
            'op_income': 224000000,
            'net_income': 157000000,
            'eps_basic': 0.23,
            'eps_diluted': 0.22,
            'dividend': 0.15,
            'assets': 13151000000,
            'cur_assets': 5179000000,
            'cur_liab': 4205000000,
            'equity': 5497000000,
            'cash': 3749000000,
            'cash_flow_op': 312000000,
            'cash_flow_inv': -29000000,
            'cash_flow_fin': -1192000000
        })

    def test_tgt_20130803(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/27419/000110465913066569/tgt-20130803.xml')
        self.assert_item(item, {
            'symbol': 'TGT',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-08-03',
            'revenues': 17117000000,
            'op_income': 1161000000,
            'net_income': 611000000,
            'eps_basic': 0.96,
            'eps_diluted': 0.95,
            'dividend': 0.43,
            'assets': 44162000000,
            'cur_assets': 11403000000,
            'cur_liab': 12616000000,
            'equity': 16020000000,
            'cash': 1018000000,
            'cash_flow_op': 4109000000,
            'cash_flow_inv': 1269000000,
            'cash_flow_fin': -5148000000
        })

    def test_trv_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/86312/000110465910021504/trv-20100331.xml')
        self.assert_item(item, {
            'symbol': 'TRV',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2010-03-31',
            'revenues': 6119000000,
            'op_income': None,
            'net_income': 647000000,
            'eps_basic': 1.26,
            'eps_diluted': 1.25,
            'dividend': 0.0,
            'assets': 108696000000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 26671000000,
            'cash': 251000000,
            'cash_flow_op': 531000000,
            'cash_flow_inv': 952000000,
            'cash_flow_fin': -1486000000
        })

    def test_tsla_20110630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1318605/000119312511221497/tsla-20110630.xml')
        self.assert_item(item, {
            'symbol': 'TSLA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2011,
            'end_date': '2011-06-30',
            'revenues': 58171000,
            'op_income': -58739000,
            'net_income': -58903000,
            'eps_basic': -0.60,
            'eps_diluted': -0.60,
            'dividend': 0.0,
            'assets': 646155000,
            'cur_assets': 417758000,
            'cur_liab': 138736000,
            'equity': 348452000,
            'cash': 319380000,
            'cash_flow_op': -65785000,
            'cash_flow_inv': -13011000,
            'cash_flow_fin': 298618000
        })

    def test_tsla_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1318605/000119312512137560/tsla-20111231.xml')
        self.assert_item(item, {
            'symbol': 'TSLA',
            'amend': True,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2011-12-31',
            'revenues': 204242000,
            'op_income': -251488000,
            'net_income': -254411000,
            'eps_basic': -2.53,
            'eps_diluted': -2.53,
            'dividend': 0.0,
            'assets': 713448000,
            'cur_assets': 372838000,
            'cur_liab': 191339000,
            'equity': 224045000,
            'cash': 255266000,
            'cash_flow_op': -114364000,
            'cash_flow_inv': -175928000,
            'cash_flow_fin': 446000000
        })

    def test_tsla_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1318605/000119312513327916/tsla-20130630.xml')
        self.assert_item(item, {
            'symbol': 'TSLA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-30',
            'revenues': 405139000,
            'op_income': -11792000,
            'net_income': -30502000,
            'eps_basic': -0.26,
            'eps_diluted': -0.26,
            'dividend': 0.0,
            'assets': 1887844000,
            'cur_assets': 1129542000,
            'cur_liab': 486545000,
            'equity': 629426000,
            'cash': 746057000,
            'cash_flow_op': 25886000,
            'cash_flow_inv': -82410000,
            'cash_flow_fin': 600691000
        })

    def test_utmd_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/706698/000109690612002585/utmd-20111231.xml')
        self.assert_item(item, {
            'symbol': 'UTMD',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2011-12-31',
            'revenues': 37860000,
            'op_income': 11842000,
            'net_income': 7414000,
            'eps_basic': 2.04,
            'eps_diluted': 2.03,
            'dividend': 0.0,
            'assets': 76389000,
            'cur_assets': 17016000,
            'cur_liab': 9631000,
            'equity': 40757000,
            'cash': 6534000,
            'cash_flow_op': 11365000,
            'cash_flow_inv': -26685000,
            'cash_flow_fin': 18078000
        })

    def test_vel_pe_20130930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/103682/000119312513427104/d-20130930.xml')
        self.assert_item(item, {
            'symbol': 'VEL - PE',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2013,
            'end_date': '2013-09-30',
            'revenues': 3432000000,
            'op_income': 1034000000,
            'net_income': 569000000,
            'eps_basic': 0.98,
            'eps_diluted': 0.98,
            'dividend': 0.5625,
            'assets': 48488000000,
            'cur_assets': 5210000000,
            'cur_liab': 6453000000,
            'equity': 11242000000,
            'cash': 287000000,
            'cash_flow_op': 2950000000,
            'cash_flow_inv': -2348000000,
            'cash_flow_fin': -563000000
        })

    def test_via_20090930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1339947/000119312509221448/via-20090930.xml')
        self.assert_item(item, {
            'symbol': 'VIA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2009,
            'end_date': '2009-09-30',
            'revenues': 3317000000,
            'op_income': 784000000,
            'net_income': 463000000,
            'eps_basic': 0.76,
            'eps_diluted': 0.76,
            'dividend': 0.0,
            'assets': 21307000000,
            'cur_assets': 3605000000,
            'cur_liab': 3707000000,
            'equity': 8044000000,
            'cash': 249000000,
            'cash_flow_op': 732000000,
            'cash_flow_inv': -117000000,
            'cash_flow_fin': -1169000000
        })

    def test_via_20091231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1339947/000119312510028165/via-20091231.xml')
        self.assert_item(item, {
            'symbol': 'VIA',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2009,
            'end_date': '2009-12-31',
            'revenues': 13619000000,
            'op_income': 2904000000,
            'net_income': 1611000000,
            'eps_basic': 2.65,
            'eps_diluted': 2.65,
            'dividend': 0.0,
            'assets': 21900000000,
            'cur_assets': 4430000000,
            'cur_liab': 3751000000,
            'equity': 8677000000,
            'cash': 298000000,
            'cash_flow_op': 1151000000,
            'cash_flow_inv': -274000000,
            'cash_flow_fin': -1388000000
        })

    def test_via_20120630(self):
        # 'via-20120401.xml' is misnamed
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1339947/000119312512333732/via-20120401.xml')
        self.assert_item(item, {
            'symbol': 'VIA',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-06-30',
            'revenues': 3241000000,
            'op_income': 903000000,
            'net_income': 534000000,
            'eps_basic': 1.02,
            'eps_diluted': 1.01,
            'dividend': 0.275,
            'assets': 21958000000,
            'cur_assets': 4511000000,
            'cur_liab': 3716000000,
            'equity': 7473000000,
            'cash': 774000000,
            'cash_flow_op': 1736000000,
            'cash_flow_inv': -212000000,
            'cash_flow_fin': -1750000000
        })

    def test_vno_20090630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/899689/000089968909000034/vno-20090630.xml')
        self.assert_item(item, {
            'symbol': 'VNO',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'FY',  # mismarked in doc, actually should be Q2
            'fiscal_year': 2009,
            'end_date': '2009-06-30',
            'revenues': 678385000,
            'op_income': 221139000,
            'net_income': -51904000,
            'eps_basic': -0.3,
            'eps_diluted': -0.3,
            'dividend': 0.95,
            'assets': 21831857000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 7122175000,
            'cash': 2068498000,
            'cash_flow_op': 379439000,
            'cash_flow_inv': -219310000,
            'cash_flow_fin': 381516000
        })

    def test_vno_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/899689/000089968912000004/vno-20111231.xml')
        self.assert_item(item, {
            'symbol': 'VNO',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2011-12-31',
            'revenues': 2915665000,
            'op_income': 856153000,
            'net_income': 601771000,
            'eps_basic': 3.26,
            'eps_diluted': 3.23,
            'dividend': 0.0,
            'assets': 20446487000,
            'cur_assets': None,
            'cur_liab': None,
            'equity': 7508447000,
            'cash': 606553000,
            'cash_flow_op': 702499000,
            'cash_flow_inv': -164761000,
            'cash_flow_fin': -621974000
        })

    def test_vrsk_20120930(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1442145/000119312512441544/vrsk-20120930.xml')
        self.assert_item(item, {
            'symbol': 'VRSK',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-30',
            'revenues': 398863000,
            'op_income': 155251000,
            'net_income': 82911000,
            'eps_basic': 0.5,
            'eps_diluted': 0.48,
            'dividend': 0.0,
            'assets': 2303433000,
            'cur_assets': 361337000,
            'cur_liab': 668257000,
            'equity': 142048000,
            'cash': 97770000,
            'cash_flow_op': 320997000,
            'cash_flow_inv': -838704000,
            'cash_flow_fin': 424004000
        })

    def test_wat_20120929(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1000697/000119312512448069/wat-20120929.xml')
        self.assert_item(item, {
            'symbol': 'WAT',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q3',
            'fiscal_year': 2012,
            'end_date': '2012-09-29',
            'revenues': 449952000,
            'op_income': 121745000,
            'net_income': 99109000,
            'eps_basic': 1.13,
            'eps_diluted': 1.12,
            'dividend': 0.0,
            'assets': 2997140000,
            'cur_assets': 2137498000,
            'cur_liab': 767562000,
            'equity': 1329879000,
            'cash': 356293000,
            'cash_flow_op': 317627000,
            'cash_flow_inv': -298851000,
            'cash_flow_fin': -53396000
        })

    def test_wec_20130331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/783325/000010781513000080/wec-20130331.xml')
        self.assert_item(item, {
            'symbol': 'WEC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2013,
            'end_date': '2013-03-31',
            'revenues': 1275200000,
            'op_income': 321000000,
            'net_income': 176600000,
            'eps_basic': 0.77,
            'eps_diluted': 0.76,
            'dividend': 0.34,
            'assets': 14295300000,
            'cur_assets': 1313800000,
            'cur_liab': 1278100000,
            'equity': 8675000000,
            'cash': 24700000,
            'cash_flow_op': 330300000,
            'cash_flow_inv': -145300000,
            'cash_flow_fin': -195900000
        })

    def test_wec_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/783325/000010781513000112/wec-20130630.xml')
        self.assert_item(item, {
            'symbol': 'WEC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-30',
            'revenues': 1012300000,
            'op_income': 229500000,
            'net_income': 119000000,
            'eps_basic': 0.52,
            'eps_diluted': 0.52,
            'dividend': 0.34,
            'assets': 14317000000,
            'cur_assets': 1271100000,
            'cur_liab': 1280700000,
            'equity': 8609000000,
            'cash': 21000000,
            'cash_flow_op': 681500000,
            'cash_flow_inv': -336600000,
            'cash_flow_fin': -359500000
        })

    def test_wfm_20120115(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/865436/000144530512000434/wfm-20120115.xml')
        self.assert_item(item, {
            'symbol': 'WFM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2012,
            'end_date': '2012-01-15',
            'revenues': 3390940000,
            'op_income': 190338000,
            'net_income': 118327000,
            'eps_basic': 0.66,
            'eps_diluted': 0.65,
            'dividend': 0.14,
            'assets': 4528241000,
            'cur_assets': 1677087000,
            'cur_liab': 896972000,
            'equity': 3182747000,
            'cash': 529954000,
            'cash_flow_op': 260896000,
            'cash_flow_inv': -6963000,
            'cash_flow_fin': 63562000
        })

    def test_xel_20100331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/72903/000110465910024080/xel-20100331.xml')
        self.assert_item(item, {
            'symbol': 'XEL',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2010,
            'end_date': '2010-03-31',
            'revenues': 2807462000,
            'op_income': 403665000,
            'net_income': 166058000,
            'eps_basic': 0.36,
            'eps_diluted': 0.36,
            'dividend': 0.25,
            'assets': 25334501000,
            'cur_assets': 2344294000,
            'cur_liab': 2759838000,
            'equity': 7355871000,
            'cash': 79504000,
            'cash_flow_op': 555539000,
            'cash_flow_inv': -460112000,
            'cash_flow_fin': -121731000
        })

    def test_xel_20101231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/72903/000114036111012444/xel-20101231.xml')
        self.assert_item(item, {
            'symbol': 'XEL',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2010,
            'end_date': '2010-12-31',
            'revenues': 10310947000,
            'op_income': 1619969000,
            'net_income': 751593000,
            'eps_basic': 1.63,
            'eps_diluted': 1.62,
            'dividend': 1.0,
            'assets': 27387690000,
            'cur_assets': 2732643000,
            'cur_liab': 2536533000,
            'equity': 8083519000,
            'cash': 108437000,
            'cash_flow_op': 1893942000,
            'cash_flow_inv': -2806724000,
            'cash_flow_fin': 905571000
        })

    def test_xom_20110331(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/34088/000119312511127973/xom-20110331.xml')
        self.assert_item(item, {
            'symbol': 'XOM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q1',
            'fiscal_year': 2011,
            'end_date': '2011-03-31',
            'revenues': 114004000000,
            'op_income': None,
            'net_income': 10650000000,
            'eps_basic': 2.14,
            'eps_diluted': 2.14,
            'dividend': 0.44,
            'assets': 319533000000,
            'cur_assets': 72022000000,
            'cur_liab': 73576000000,
            'equity': 157531000000,
            'cash': 12833000000,
            'cash_flow_op': 16856000000,
            'cash_flow_inv': -5353000000,
            'cash_flow_fin': -6749000000
        })

    def test_xom_20111231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/34088/000119312512078102/xom-20111231.xml')
        self.assert_item(item, {
            'symbol': 'XOM',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2011,
            'end_date': '2011-12-31',
            'revenues': 467029000000,
            'op_income': None,
            'net_income': 41060000000,
            'eps_basic': 8.43,
            'eps_diluted': 8.42,
            'dividend': 1.85,
            'assets': 331052000000,
            'cur_assets': 72963000000,
            'cur_liab': 77505000000,
            'equity': 160744000000,
            'cash': 12664000000,
            'cash_flow_op': 55345000000,
            'cash_flow_inv': -22165000000,
            'cash_flow_fin': -28256000000
        })

    def test_xom_20130630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/34088/000003408813000035/xom-20130630.xml')
        self.assert_item(item, {
            'symbol': 'XOM',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-30',
            'revenues': 106469000000,
            'op_income': None,
            'net_income': 6860000000,
            'eps_basic': 1.55,
            'eps_diluted': 1.55,
            'dividend': 0.63,
            'assets': 341615000000,
            'cur_assets': 62844000000,
            'cur_liab': 72688000000,
            'equity': 171588000000,
            'cash': 4609000000,
            'cash_flow_op': 21275000000,
            'cash_flow_inv': -18547000000,
            'cash_flow_fin': -7409000000
        })

    def test_xray_20091231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/818479/000114420410009164/xray-20091231.xml')
        self.assert_item(item, {
            'symbol': 'XRAY',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2009,
            'end_date': '2009-12-31',
            'revenues': 2159916000,
            'op_income': 381187000,
            'net_income': 274258000,
            'eps_basic': 1.85,
            'eps_diluted': 1.83,
            'dividend': 0.2,
            'assets': 3087932000,
            'cur_assets': 1217796000,
            'cur_liab': 444556000,
            'equity': 1906958000,
            'cash': 450348000,
            'cash_flow_op': 362489000,
            'cash_flow_inv': -53399000,
            'cash_flow_fin': -71420000
        })

    def test_xrx_20091231(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/108772/000119312510043079/xrx-20091231.xml')
        self.assert_item(item, {
            'symbol': 'XRX',
            'amend': False,
            'doc_type': '10-K',
            'period_focus': 'FY',
            'fiscal_year': 2009,
            'end_date': '2009-12-31',
            'revenues': 15179000000,
            'op_income': None,
            'net_income': 485000000,
            'eps_basic': 0.56,
            'eps_diluted': 0.55,
            'dividend': 0.0,
            'assets': 24032000000,
            'cur_assets': 9731000000,
            'cur_liab': 4461000000,
            'equity': 7191000000,
            'cash': 3799000000,
            'cash_flow_op': 2208000000,
            'cash_flow_inv': -343000000,
            'cash_flow_fin': 692000000
        })

    def test_zmh_20090630(self):
        item = parse_xml('http://www.sec.gov/Archives/edgar/data/1136869/000095012309035693/zmh-20090630.xml')
        self.assert_item(item, {
            'symbol': 'ZMH',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2009,
            'end_date': '2009-06-30',
            'revenues': 1019900000,
            'op_income': 296499999.99999988,
            'net_income': 210099999.99999988,  # Wired number, but it's actually in the filing
            'eps_basic': 0.98,
            'eps_diluted': 0.98,
            'dividend': 0.0,
            'assets': 7462100000.000001,
            'cur_assets': 2328700000.0000005,
            'cur_liab': 669200000,
            'equity': 5805600000,
            'cash': 277500000,
            'cash_flow_op': 379700000.00000018,
            'cash_flow_inv': -174300000.00000003,
            'cash_flow_fin': -142000000.00000003
        })
