from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import XmlXPathSelector

from stockcrawler.items import StockItem


def find_namespace(xxs, name):
    name_re = name.replace('-', '\-')
    if not name_re.startswith('xmlns'):
        name_re = 'xmlns:' + name_re
    return xxs.re('%s=\"([^\"]+)\"' % name_re)[0]


def register_namespace(xxs, name):
    ns = find_namespace(xxs, name)
    xxs.register_namespace(name, ns)


def register_namespaces(xxs):
    names = ('xmlns', 'xbrli', 'dei', 'us-gaap')
    for name in names:
        try:
            register_namespace(xxs, name)
        except IndexError:
            pass


def load_symbols(file_path):
    symbols = []
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                symbols.append(line)
    return symbols


class URLGenerator(object):

    def __init__(self, symbols):
        self.symbols = symbols

    def __iter__(self):
        url = 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=10-&dateb=&owner=exclude&count=300'
        for symbol in self.symbols:
            yield (url % symbol)

# http://www.sec.gov/Archives/edgar/data/1326801/000132680113000019/0001326801-13-000019-index.htm
# http://www.sec.gov/Archives/edgar/data/1326801/000132680113000019/fb-6302013x10q.htm
# http://www.sec.gov/Archives/edgar/data/1288776/000119312509101727/d10q.htm
# http://www.sec.gov/Archives/edgar/data/1288776/000119312504142809/0001193125-04-142809-index.htm
# http://www.sec.gov/Archives/edgar/data/1288776/000119312504141838/0001193125-04-141838-index.htm
# http://www.sec.gov/Archives/edgar/data/1288776/000119312504142809/d10qa.htm
# http://www.sec.gov/Archives/edgar/data/1288776/000128877613000055/goog-20130630.xml
# http://www.sec.gov/Archives/edgar/data/1288776/000119312512182401/goog-20120331.xml


class EdgarSpider(CrawlSpider):

    name = 'edgar'
    allowed_domains = ['sec.gov']

    rules = (
        Rule(SgmlLinkExtractor(allow=('/Archives/edgar/data/[^\"]+\-index\.htm',))),
        Rule(SgmlLinkExtractor(allow=('/Archives/edgar/data/[^\"]+\-\d{8}\.xml',)), callback='parse_10q'),
    )

    def __init__(self, **kwargs):
        super(EdgarSpider, self).__init__(**kwargs)

        symbol_file_path = kwargs.get('symbols')
        if symbol_file_path:
            symbols = load_symbols(symbol_file_path)
            self.start_urls = URLGenerator(symbols)
        else:
            self.start_urls = []

    def parse_10q(self, response):
        xxs = XmlXPathSelector(response)
        register_namespaces(xxs)

        items = []

        # extract symbol
        symbol = xxs.select('//dei:TradingSymbol/text()')[0].extract().upper()

        # extract outstanding shares
        for s in xxs.select('//dei:EntityCommonStockSharesOutstanding'):
            num_shares = int(s.select('text()')[0].extract())

            context_id = s.select('@contextRef')[0].extract()
            context = xxs.select('//*[@id="%s"]' % context_id)[0]

            date = context.select('.//*[local-name()="instant"]/text()')[0].extract()

            try:
                class_str = context.select('.//*[local-name()="explicitMember"]/text()')[0].extract()
            except IndexError:
                stock_class = 'A'
            else:
                if 'ClassB' in class_str:
                    stock_class = 'B'
                else:
                    stock_class = 'A'

            item = StockItem()
            item['symbol'] = symbol
            item['key'] = 'NUM_SHARES_' + stock_class
            item['value'] = num_shares
            item['date'] = date
            items.append(item)

        # extract EPS
        for s in xxs.select('//us-gaap:EarningsPerShareBasic'):
            eps = float(s.select('text()')[0].extract())

            context_id = s.select('@contextRef')[0].extract()
            context = xxs.select('//*[@id="%s"]' % context_id)[0]

            start_date = context.select('.//*[local-name()="startDate"]/text()')[0].extract()
            end_date = context.select('.//*[local-name()="endDate"]/text()')[0].extract()

            item = StockItem()
            item['symbol'] = symbol
            item['key'] = 'EPS_BASIC'
            item['value'] = eps
            item['date'] = '%s:%s' % (start_date, end_date)
            items.append(item)

        for s in xxs.select('//us-gaap:EarningsPerShareDiluted'):
            eps = float(s.select('text()')[0].extract())

            context_id = s.select('@contextRef')[0].extract()
            context = xxs.select('//*[@id="%s"]' % context_id)[0]

            start_date = context.select('.//*[local-name()="startDate"]/text()')[0].extract()
            end_date = context.select('.//*[local-name()="endDate"]/text()')[0].extract()

            item = StockItem()
            item['symbol'] = symbol
            item['key'] = 'EPS_DILUTED'
            item['value'] = eps
            item['date'] = '%s:%s' % (start_date, end_date)
            items.append(item)

        # extract dividend
        for s in xxs.select('//us-gaap:CommonStockDividendsPerShareDeclared'):
            div = float(s.select('text()')[0].extract())

            context_id = s.select('@contextRef')[0].extract()
            context = xxs.select('//*[@id="%s"]' % context_id)[0]

            start_date = context.select('.//*[local-name()="startDate"]/text()')[0].extract()
            end_date = context.select('.//*[local-name()="endDate"]/text()')[0].extract()

            item = StockItem()
            item['symbol'] = symbol
            item['key'] = 'DIVIDEND'
            item['value'] = div
            item['date'] = '%s:%s' % (start_date, end_date)
            items.append(item)

        # extract revenue
        all_revs = {}
        for s in xxs.select('//us-gaap:Revenues'):
            rev = float(s.select('text()')[0].extract())

            context_id = s.select('@contextRef')[0].extract()
            context = xxs.select('//*[@id="%s"]' % context_id)[0]

            start_date = context.select('.//*[local-name()="startDate"]/text()')[0].extract()
            end_date = context.select('.//*[local-name()="endDate"]/text()')[0].extract()

            date = '%s:%s' % (start_date, end_date)

            existing_rev = all_revs.get(date)
            if rev > existing_rev:
                all_revs[date] = rev

        for date, rev in all_revs.iteritems():
            item = StockItem()
            item['symbol'] = symbol
            item['key'] = 'REVENUES'
            item['value'] = rev
            item['date'] = date
            items.append(item)

        # extract net income
        all_incomes = {}
        for s in xxs.select('//us-gaap:NetIncomeLoss'):
            income = float(s.select('text()')[0].extract())

            context_id = s.select('@contextRef')[0].extract()
            context = xxs.select('//*[@id="%s"]' % context_id)[0]

            start_date = context.select('.//*[local-name()="startDate"]/text()')[0].extract()
            end_date = context.select('.//*[local-name()="endDate"]/text()')[0].extract()

            date = '%s:%s' % (start_date, end_date)

            existing_income = all_incomes.get(date)
            if income > existing_income:
                all_incomes[date] = income

        for date, income in all_incomes.iteritems():
            item = StockItem()
            item['symbol'] = symbol
            item['key'] = 'NET_INCOME'
            item['value'] = income
            item['date'] = date
            items.append(item)

        return items
