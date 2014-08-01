import os
import tempfile

from scrapy.http import HtmlResponse, XmlResponse

from pystock_crawler.spiders.edgar import EdgarSpider, URLGenerator
from pystock_crawler.tests.base import TestCaseBase


def make_url(symbol, start_date='', end_date=''):
    '''A URL that lists all 10-Q and 10-K filings of a company.'''
    return 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=10-&dateb=%s&datea=%s&owner=exclude&count=300' \
           % (symbol, end_date, start_date)


def make_link_html(href, text=u'Link'):
    return u'<a href="%s">%s</a>' % (href, text)


class URLGeneratorTest(TestCaseBase):

    def test_no_dates(self):
        urls = URLGenerator(('FB', 'GOOG'))
        self.assertEqual(list(urls), [
            make_url('FB'), make_url('GOOG')
        ])

    def test_with_start_date(self):
        urls = URLGenerator(('AAPL', 'AMZN', 'GLD'), start_date='20120215')
        self.assertEqual(list(urls), [
            make_url('AAPL', start_date='20120215'),
            make_url('AMZN', start_date='20120215'),
            make_url('GLD', start_date='20120215')
        ])

    def test_with_end_date(self):
        urls = URLGenerator(('TSLA', 'USO', 'MMM'), end_date='20110530')
        self.assertEqual(list(urls), [
            make_url('TSLA', end_date='20110530'),
            make_url('USO', end_date='20110530'),
            make_url('MMM', end_date='20110530')
        ])

    def test_with_start_and_end_dates(self):
        urls = URLGenerator(('DDD', 'AXP', 'KO'), start_date='20111230', end_date='20121230')
        self.assertEqual(list(urls), [
            make_url('DDD', '20111230', '20121230'),
            make_url('AXP', '20111230', '20121230'),
            make_url('KO', '20111230', '20121230')
        ])


class EdgarSpiderTest(TestCaseBase):

    def test_empty_creation(self):
        spider = EdgarSpider()
        self.assertEqual(spider.start_urls, [])

    def test_symbol_file(self):
        # create a mock file of a list of symbols
        f = tempfile.NamedTemporaryFile('w', delete=False)
        f.write('# Comment\nGOOG\nADBE\nLNKD\n#comment\nJPM\n')
        f.close()

        spider = EdgarSpider(symbols=f.name)
        urls = list(spider.start_urls)

        self.assertEqual(urls, [
            make_url('GOOG'), make_url('ADBE'),
            make_url('LNKD'), make_url('JPM')
        ])

        os.remove(f.name)

    def test_invalid_dates(self):
        with self.assertRaises(ValueError):
            EdgarSpider(startdate='12345678')

        with self.assertRaises(ValueError):
            EdgarSpider(enddate='12345678')

    def test_symbol_file_and_dates(self):
        # create a mock file of a list of symbols
        f = tempfile.NamedTemporaryFile('w', delete=False)
        f.write('# Comment\nT\nCBS\nWMT\n')
        f.close()

        spider = EdgarSpider(symbols=f.name, startdate='20110101', enddate='20130630')
        urls = list(spider.start_urls)

        self.assertEqual(urls, [
            make_url('T', '20110101', '20130630'),
            make_url('CBS', '20110101', '20130630'),
            make_url('WMT', '20110101', '20130630')
        ])

        os.remove(f.name)

    def test_parse_company_filing_page(self):
        '''
        Parse the page that lists all filings of a company.

        Example:
        http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001288776&type=10-&dateb=&owner=exclude&count=40

        '''
        spider = EdgarSpider()
        spider._follow_links = True  # HACK

        body = '''
            <html><body>
            <a href="http://example.com/">Useless Link</a>
            <a href="/Archives/edgar/data/abc-index.htm">Link</a>
            <a href="/Archives/edgar/data/123-index.htm">Link</a>
            <a href="/Archives/edgar/data/123.htm">Useless Link</a>
            <a href="/Archives/edgar/data/123/abc-index.htm">Link</a>
            <a href="/Archives/edgar/data/123/456/abc123-index.htm">Link</a>
            <a href="/Archives/edgar/123/abc-index.htm">Uselss Link</a>
            <a href="/Archives/edgar/data/123/456/789/HELLO-index.htm">Link</a>
            <a href="/Archives/hello-index.html">Useless Link</a>
            </body></html>
        '''

        response = HtmlResponse('http://sec.gov/mock', body=body)
        requests = spider.parse(response)
        urls = [r.url for r in requests]

        self.assertEqual(urls, [
            'http://sec.gov/Archives/edgar/data/abc-index.htm',
            'http://sec.gov/Archives/edgar/data/123-index.htm',
            'http://sec.gov/Archives/edgar/data/123/abc-index.htm',
            'http://sec.gov/Archives/edgar/data/123/456/abc123-index.htm',
            'http://sec.gov/Archives/edgar/data/123/456/789/HELLO-index.htm'
        ])

    def test_parse_quarter_or_annual_page(self):
        '''
        Parse the page that lists filings of a quater or a year of a company.

        Example:
        http://www.sec.gov/Archives/edgar/data/1288776/000128877613000055/0001288776-13-000055-index.htm

        '''
        spider = EdgarSpider()
        spider._follow_links = True  # HACK

        body = '''
            <html><body>
            <a href="http://example.com">Useless Link</a>
            <a href="/Archives/edgar/data/123/abc-20130630.xml">Link</a>
            <a href="/Archives/edgar/123/456/abc123-20130630.xml">Useless Link</a>
            <a href="/Archives/edgar/data/456/789/hello-20130630.xml">Link</a>
            <a href="/Archives/edgar/123/456/hello-20130630.xml">Useless Link</a>
            <a href="/Archives/data/123/456/hello-20130630.xml">Useless Link</a>
            <a href="/Archives/edgar/data/123/456/hello-201306300.xml">Useless Link</a>
            <a href="/Archives/edgar/data/123/456/xyz-20130630.html">Link</a>
            </body></html>
        '''

        response = HtmlResponse('http://sec.gov/mock', body=body)
        requests = spider.parse(response)
        urls = [r.url for r in requests]

        self.assertEqual(urls, [
            'http://sec.gov/Archives/edgar/data/123/abc-20130630.xml',
            'http://sec.gov/Archives/edgar/data/456/789/hello-20130630.xml'
        ])

    def test_parse_xml_report(self):
        '''Parse XML 10-Q or 10-K report.'''
        spider = EdgarSpider()
        spider._follow_links = True  # HACK

        body = '''
            <?xml version="1.0">
            <xbrl xmlns="http://www.xbrl.org/2003/instance"
                  xmlns:xbrli="http://www.xbrl.org/2003/instance"
                  xmlns:dei="http://xbrl.sec.gov/dei/2011-01-31"
                  xmlns:us-gaap="http://fasb.org/us-gaap/2011-01-31">

              <context id="c1">
                <startDate>2013-03-31</startDate>
                <endDate>2013-06-28</endDate>
              </context>

              <dei:AmendmentFlag contextRef="c1">false</dei:AmendmentFlag>
              <dei:DocumentType contextRef="c1">10-Q</dei:DocumentType>
              <dei:DocumentFiscalPeriodFocus contextRef="c1">Q2</dei:DocumentFiscalPeriodFocus>
              <dei:DocumentPeriodEndDate contextRef="c1">2013-06-28</dei:DocumentPeriodEndDate>
              <dei:DocumentFiscalYearFocus>2013</dei>

              <us-gaap:Revenues contextRef="c1">100</us-gaap:Revenues>
              <us-gaap:NetIncomeLoss contextRef="c1">200</us-gaap:NetIncomeLoss>
              <us-gaap:EarningsPerShareBasic contextRef="c1">0.2</us-gaap:EarningsPerShareBasic>
              <us-gaap:EarningsPerShareDiluted contextRef="c1">0.19</us-gaap:EarningsPerShareDiluted>
              <us-gaap:CommonStockDividendsPerShareDeclared contextRef="c1">0.07</us-gaap:CommonStockDividendsPerShareDeclared>

              <us-gaap:Assets contextRef="c1">1600</us-gaap:Assets>
              <us-gaap:StockholdersEquity contextRef="c1">300</us-gaap:StockholdersEquity>
              <us-gaap:CashAndCashEquivalentsAtCarryingValue contextRef="c1">150</us-gaap:CashAndCashEquivalentsAtCarryingValue>
            </xbrl>
        '''

        response = XmlResponse('http://sec.gov/Archives/edgar/data/123/abc-20130720.xml', body=body)
        item = spider.parse_10qk(response)

        self.assert_item(item, {
            'symbol': 'ABC',
            'amend': False,
            'doc_type': '10-Q',
            'period_focus': 'Q2',
            'fiscal_year': 2013,
            'end_date': '2013-06-28',
            'revenues': 100.0,
            'net_income': 200.0,
            'eps_basic': 0.2,
            'eps_diluted': 0.19,
            'dividend': 0.07,
            'assets': 1600.0,
            'equity': 300.0,
            'cash': 150.0
        })
