from datetime import datetime
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Compose, MapCompose, TakeFirst
from scrapy.selector import XmlXPathSelector
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import flatten

from stockcrawler.items import ReportItem


class ExtractText(object):

    def __call__(self, value):
        if hasattr(value, 'select'):
            return value.select('./text()')[0].extract()
        return unicode(value)


class MatchEndDate(object):

    def __init__(self, data_type=str, context_filter=None):
        self.data_type = data_type
        self.context_filter = context_filter

    def __call__(self, value, loader_context):
        if not hasattr(value, 'select'):
            return value

        doc_end_date = loader_context['end_date']
        doc_type = loader_context['doc_type']
        selector = loader_context['selector']

        context_id = value.select('@contextRef')[0].extract()
        context = selector.select('//*[@id="%s"]' % context_id)[0]

        if self.context_filter and not self.context_filter(context):
            return None

        date = None
        try:
            date = context.select('.//*[local-name()="instant"]/text()')[0].extract()
        except IndexError:
            try:
                start_date_str = context.select('.//*[local-name()="startDate"]/text()')[0].extract()
                end_date_str = context.select('.//*[local-name()="endDate"]/text()')[0].extract()
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                delta_days = (end_date - start_date).days
                if doc_type == '10-Q' and delta_days < 95 and delta_days > 85:
                    date = end_date_str
                elif doc_type == '10-K' and delta_days < 380 and delta_days > 350:
                    date = end_date_str
            except IndexError:
                pass

        if doc_end_date == date:
            return self.data_type(value.select('./text()')[0].extract())

        return None


class FindSum(object):

    def __call__(self, values):
        print 'values: %s' % str(values)

        size = len(values)
        if size == 1:
            return values[0]
        elif size == 2:
            return max(values)

        for i in xrange(0, size):
            value = values[i]
            if value == sum(values) - value:
                return value

        return None


class ZeroIfNone(object):

    def __call__(self, value):
        return 0.0 if value is None else value


def exclude_member(context):
    try:
        context.select('.//*[local-name()="explicitMember"]/text()')[0]
    except IndexError:
        return True
    return False


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


class XmlXPathItemLoader(XPathItemLoader):

    default_selector_class = XmlXPathSelector

    def __init__(self, *args, **kwargs):
        super(XmlXPathItemLoader, self).__init__(*args, **kwargs)
        register_namespaces(self.selector)

    def add_xpath(self, field_name, xpath, *processors, **kw):
        values = self._get_values(xpath, **kw)
        self.add_value(field_name, values, *processors, **kw)
        return len(values)

    def add_xpaths(self, name_path_pairs):
        for name, path in name_path_pairs:
            match_count = self.add_xpath(name, path)
            if match_count > 0:
                return match_count
        return 0

    def _get_values(self, xpaths, **kw):
        xpaths = arg_to_iter(xpaths)
        return flatten([self.selector.select(xpath) for xpath in xpaths])


class ReportLoader(XmlXPathItemLoader):

    default_item_class = ReportItem
    default_output_processor = TakeFirst()

    symbol_in = MapCompose(ExtractText(), unicode.upper)
    period_focus_in = MapCompose(ExtractText(), unicode.upper)

    revenues_in = MapCompose(MatchEndDate(float))
    revenues_out = Compose(max)

    net_income_in = MapCompose(MatchEndDate(float))
    net_income_out = Compose(max)

    num_shares_in = MapCompose(MatchEndDate(int))
    num_shares_out = Compose(max)

    eps_basic_in = MapCompose(MatchEndDate(float))

    eps_diluted_in = MapCompose(MatchEndDate(float))

    dividend_in = MapCompose(MatchEndDate(float))

    assets_in = MapCompose(MatchEndDate(float, context_filter=exclude_member))
    assets_out = Compose(max)

    equity_in = MapCompose(MatchEndDate(float), context_filter=exclude_member)
    equity_out = TakeFirst()

    cash_in = MapCompose(MatchEndDate(float))
    cash_out = Compose(max)

    def __init__(self, *args, **kwargs):
        super(ReportLoader, self).__init__(*args, **kwargs)

        symbol = self._get_symbol()
        end_date = self._get_doc_end_date()
        doc_type = self._get_doc_type()

        self.context.update({
            'end_date': end_date,
            'doc_type': doc_type
        })

        self.add_xpath('symbol', '//dei:TradingSymbol')
        self.add_value('symbol', symbol)

        self.add_value('end_date', end_date)
        self.add_value('doc_type', doc_type)

        if not self.add_xpath('period_focus', '//dei:DocumentFiscalPeriodFocus'):
            period_focus = self._get_period_focus(end_date)
            self.add_value('period_focus', period_focus)

        self.add_xpath('revenues', '//us-gaap:Revenues')
        self.add_xpath('revenues', '//us-gaap:SalesRevenueNet')
        self.add_xpath('revenues', '//us-gaap:SalesRevenueGoodsNet')

        self.add_xpaths([
            ('net_income', '//us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic'),
            ('net_income', '//us-gaap:NetIncomeLoss')
        ])

        self.add_xpath('num_shares', '//us-gaap:WeightedAverageNumberOfSharesOutstandingBasic')

        self.add_xpath('eps_basic', '//us-gaap:EarningsPerShareBasic')
        self.add_xpath('eps_diluted', '//us-gaap:EarningsPerShareDiluted')

        self.add_xpaths([
            ('dividend', '//us-gaap:CommonStockDividendsPerShareCashPaid'),
            ('dividend', '//us-gaap:CommonStockDividendsPerShareDeclared')
        ])
        self.add_value('dividend', 0.0)

        self.add_xpath('assets', '//us-gaap:Assets')

        self.add_xpaths([
            ('equity', '//us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest'),
            ('equity', '//us-gaap:StockholdersEquity')
        ])

        self.add_xpaths([
            ('cash', '//us-gaap:CashAndDueFromBanks'),
            ('cash', '//us-gaap:CashAndCashEquivalentsAtCarryingValue')
        ])

    def _get_symbol(self):
        try:
            filename = self.context['response'].url.split('/')[-1]
            return filename.split('-')[0].upper()
        except IndexError:
            return None

    def _get_doc_end_date(self):
        return self.selector.select('//dei:DocumentPeriodEndDate/text()')[0].extract()

    def _get_doc_type(self):
        return self.selector.select('//dei:DocumentType/text()')[0].extract().upper()

    def _get_period_focus(self, doc_end_date):
        try:
            doc_yr = doc_end_date.split('-')[0]
            yr_end_date = self.selector.select('//dei:CurrentFiscalYearEndDate/text()')[0].extract()
            yr_end_date = yr_end_date.replace('--', doc_yr + '-')
        except IndexError:
            return None

        doc_end_date = datetime.strptime(doc_end_date, '%Y-%m-%d')
        yr_end_date = datetime.strptime(yr_end_date, '%Y-%m-%d')
        delta_days = (yr_end_date - doc_end_date).days

        if delta_days > -45 and delta_days < 45:
            return 'FY'
        elif delta_days > -135 and delta_days < 135:
            return 'Q3'
        elif delta_days > -225 and delta_days < 225:
            return 'Q2'
        elif delta_days > -315 and delta_days < 315:
            return 'Q1'

        return 'FY'
