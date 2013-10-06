from datetime import datetime
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from stockcrawler.loaders import ReportItemLoader


def load_symbols(file_path):
    symbols = []
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                symbols.append(line)
    return symbols


def check_date_arg(value, arg_name):
    if value:
        try:
            datetime.strptime(value, '%Y%m%d')
        except ValueError:
            raise ValueError("Option '%s' must be in YYYYMMDD format, input is '%s'" % (arg_name, value))


class URLGenerator(object):

    def __init__(self, symbols, start_date='', end_date=''):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date

    def __iter__(self):
        url = 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=10-&dateb=%s&datea=%s&owner=exclude&count=300'
        for symbol in self.symbols:
            yield (url % (symbol, self.end_date, self.start_date))

# http://www.sec.gov/Archives/edgar/data/1326801/000132680113000019/0001326801-13-000019-index.htm
# http://www.sec.gov/Archives/edgar/data/1326801/000132680113000019/fb-6302013x10q.htm
# http://www.sec.gov/Archives/edgar/data/1288776/000119312509101727/d10q.htm
# http://www.sec.gov/Archives/edgar/data/1288776/000119312504142809/0001193125-04-142809-index.htm
# http://www.sec.gov/Archives/edgar/data/1288776/000119312504141838/0001193125-04-141838-index.htm
# http://www.sec.gov/Archives/edgar/data/1288776/000119312504142809/d10qa.htm
# http://www.sec.gov/Archives/edgar/data/1288776/000128877613000055/goog-20130630.xml
# http://www.sec.gov/Archives/edgar/data/1288776/000119312512182401/goog-20120331.xml
# http://www.sec.gov/Archives/edgar/data/789019/000119312511200680/msft-20110630.xml


class EdgarSpider(CrawlSpider):

    name = 'edgar'
    allowed_domains = ['sec.gov']

    rules = (
        Rule(SgmlLinkExtractor(allow=('/Archives/edgar/data/[^\"]+\-index\.htm',))),
        Rule(SgmlLinkExtractor(allow=('/Archives/edgar/data/[^\"]+\-\d{8}\.xml',)), callback='parse_10qk'),
    )

    def __init__(self, **kwargs):
        super(EdgarSpider, self).__init__(**kwargs)

        symbol_file_path = kwargs.get('symbols')
        start_date = kwargs.get('startdate', '')
        end_date = kwargs.get('enddate', '')

        check_date_arg(start_date, 'startdate')
        check_date_arg(end_date, 'enddate')

        if symbol_file_path:
            symbols = load_symbols(symbol_file_path)
            self.start_urls = URLGenerator(symbols, start_date, end_date)
        else:
            self.start_urls = []

    def parse_10qk(self, response):
        '''Parse 10-Q or 10-K XML report.'''
        loader = ReportItemLoader(response=response)
        return loader.load_item()
