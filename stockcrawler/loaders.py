from datetime import datetime
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Compose, MapCompose, TakeFirst
from scrapy.selector import XmlXPathSelector
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import flatten

from stockcrawler.items import ReportItem


DATE_FORMAT = '%Y-%m-%d'


class IntermediateValue(object):
    '''
    Intermediate data that serves as output of input processors, i.e., input
    of output processors. "Intermediate" is shorten as "imd" in later naming.

    '''
    def __init__(self, value, context):
        self.value = value
        self.context = context

    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0

    def __repr__(self):
        return '(%s, %s)' % (self.value, self.context.select('@id')[0].extract())

    def is_member(self):
        return is_member(self.context)


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
            return IntermediateValue(0.0, None)

        doc_end_date_str = loader_context['end_date']
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
                start_date = datetime.strptime(start_date_str, DATE_FORMAT)
                end_date = datetime.strptime(end_date_str, DATE_FORMAT)
                delta_days = (end_date - start_date).days
                if doc_type == '10-Q' and delta_days < 120 and delta_days > 60:
                    date = end_date
                elif doc_type == '10-K' and delta_days < 380 and delta_days > 350:
                    date = end_date
            except IndexError:
                pass
        else:
            date = datetime.strptime(date, DATE_FORMAT)

        if date:
            doc_end_date = datetime.strptime(doc_end_date_str, DATE_FORMAT)
            delta_days = (doc_end_date - date).days
            if abs(delta_days) < 30:
                try:
                    val = self.data_type(value.select('./text()')[0].extract())
                except IndexError:
                    pass
                else:
                    return IntermediateValue(val, context)

        return None


class ImdTakeFirst(object):

    def __call__(self, imd_values):
        if imd_values:
            return imd_values[0].value
        return None


class ImdSumMembersOr(object):

    def __init__(self, second_func=None):
        self.second_func = second_func

    def __call__(self, imd_values):
        members = []
        non_members = []
        for imd_value in imd_values:
            if imd_value.is_member():
                members.append(imd_value)
            else:
                non_members.append(imd_value)

        if members and len(members) == len(imd_values):
            return sum([m.value for m in members])

        if imd_values:
            return self.second_func(non_members)
        return None


def imd_first(imd_values):
    if imd_values:
        return imd_values[0].value
    return None


def imd_max(imd_values):
    if imd_values:
        imd_value = max(imd_values)
        return imd_value.value
    return None


def imd_min(imd_values):
    if imd_values:
        imd_value = min(imd_values)
        return imd_value.value
    return None


def is_member(context):
    if context:
        texts = context.select('.//*[local-name()="explicitMember"]/text()').extract()
        text = str(texts).lower()

        # 'SuccessorMember' is a rare case that shouldn't be treated as member
        if 'member' not in text or 'successormember' in text:
            return False
    return True


def is_not_member(context):
    return not is_member(context)


def str_to_bool(value):
    if hasattr(value, 'lower'):
        value = value.lower()
        return value and value != 'false' and value != '0'
    return bool(value)


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
        return len(self._values[field_name])

    def add_xpaths(self, name, paths):
        for path in paths:
            match_count = self.add_xpath(name, path)
            if match_count > 0:
                return match_count

        return 0

    def _get_values(self, xpaths, **kw):
        xpaths = arg_to_iter(xpaths)
        return flatten([self.selector.select(xpath) for xpath in xpaths])


class ReportItemLoader(XmlXPathItemLoader):

    default_item_class = ReportItem
    default_output_processor = TakeFirst()

    symbol_in = MapCompose(ExtractText(), unicode.upper)
    symbol_out = TakeFirst()

    amend_in = MapCompose(ExtractText(), str_to_bool)
    amend_out = TakeFirst()

    period_focus_in = MapCompose(ExtractText(), unicode.upper)
    period_focus_out = TakeFirst()

    revenues_in = MapCompose(MatchEndDate(float))
    revenues_out = ImdSumMembersOr(imd_max)

    net_income_in = MapCompose(MatchEndDate(float, context_filter=is_not_member))
    net_income_out = Compose(imd_min)

    eps_basic_in = MapCompose(MatchEndDate(float))
    eps_basic_out = ImdSumMembersOr(imd_first)

    eps_diluted_in = MapCompose(MatchEndDate(float))
    eps_diluted_out = ImdSumMembersOr(imd_first)

    dividend_in = MapCompose(MatchEndDate(float))
    dividend_out = ImdTakeFirst()

    assets_in = MapCompose(MatchEndDate(float, context_filter=is_not_member))
    assets_out = Compose(imd_max)

    equity_in = MapCompose(MatchEndDate(float, context_filter=is_not_member))
    equity_out = ImdTakeFirst()

    cash_in = MapCompose(MatchEndDate(float))
    cash_out = Compose(imd_max)

    def __init__(self, *args, **kwargs):
        super(ReportItemLoader, self).__init__(*args, **kwargs)

        symbol = self._get_symbol()
        end_date = self._get_doc_end_date()
        doc_type = self._get_doc_type()

        # some documents set their amendment flag in DocumentType, e.g., '10-Q/A',
        # instead of setting it in AmendmentFlag
        amend = None
        if doc_type.endswith('/A'):
            amend = True
            doc_type = doc_type[0:-2]

        self.context.update({
            'end_date': end_date,
            'doc_type': doc_type
        })

        self.add_xpath('symbol', '//dei:TradingSymbol')
        self.add_value('symbol', symbol)

        if amend:
            self.add_value('amend', True)
        else:
            self.add_xpath('amend', '//dei:AmendmentFlag')

        self.add_value('end_date', end_date)
        self.add_value('doc_type', doc_type)

        if not self.add_xpath('period_focus', '//dei:DocumentFiscalPeriodFocus'):
            period_focus = self._get_period_focus(end_date)
            self.add_value('period_focus', period_focus)

        self.add_xpaths('revenues', [
            '//us-gaap:Revenues',
            '//us-gaap:SalesRevenueNet',
            '//us-gaap:SalesRevenueGoodsNet',
            '//us-gaap:SalesRevenueServicesNet',
            '//*[contains(local-name(), "TotalRevenues") and contains(local-name(), "After")]',
            '//*[contains(local-name(), "TotalRevenues")]'
        ])
        self.add_xpath('revenues', '//us-gaap:FinancialServicesRevenue')

        self.add_xpaths('net_income', [
            '//us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic',
            '//us-gaap:NetIncomeLoss',
            '//us-gaap:ProfitLoss'
        ])

        self.add_xpaths('eps_basic', [
            '//us-gaap:EarningsPerShareBasic',
            '//us-gaap:IncomeLossFromContinuingOperationsPerBasicShare',
            '//us-gaap:IncomeLossFromContinuingOperationsPerBasicAndDilutedShare',
            '//*[local-name()="BasicEarningsPerShare"]',
            '//*[local-name()="BasicEarningsAttributableToStockholdersPerCommonShare"]',
            '//*[local-name()="IncomePerShareFromContinuingOperationsAvailableToCompanyStockholdersBasicAndDiluted"]',
            '//us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic',
            '//us-gaap:EarningsPerShareBasicAndDiluted',
            '//*[contains(local-name(), "EarningsPerShareBasic")]',
            '//*[contains(local-name(), "NetLossPerShare")]'
        ])

        self.add_xpaths('eps_diluted', [
            '//us-gaap:EarningsPerShareDiluted',
            '//us-gaap:IncomeLossFromContinuingOperationsPerDilutedShare',
            '//us-gaap:IncomeLossFromContinuingOperationsPerBasicAndDilutedShare',
            '//*[local-name()="DilutedEarningsPerShare"]',
            '//*[local-name()="DilutedEarningsAttributableToStockholdersPerCommonShare"]',
            '//*[local-name()="IncomePerShareFromContinuingOperationsAvailableToCompanyStockholdersBasicAndDiluted"]',
            '//us-gaap:NetIncomeLossAvailableToCommonStockholdersDiluted',
            '//us-gaap:EarningsPerShareBasicAndDiluted',
            '//*[contains(local-name(), "EarningsPerShareDiluted")]',
            '//*[contains(local-name(), "EarningsPerShareBasicAndDiluted")]',
            '//*[contains(local-name(), "NetLossPerShare")]'
        ])

        self.add_xpaths('dividend', [
            '//us-gaap:CommonStockDividendsPerShareCashPaid',
            '//us-gaap:CommonStockDividendsPerShareDeclared'
        ])

        # if dividend isn't found in doc, assume it's 0
        self.add_value('dividend', 0.0)

        self.add_xpath('assets', '//us-gaap:Assets')

        self.add_xpaths('equity', [
            '//us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest',
            '//us-gaap:StockholdersEquity',
            '//us-gaap:RetainedEarningsAccumulatedDeficit',
            '//*[contains(local-name(), "MembersEquityIncludingPortionAttributableToNoncontrollingInterest")]'
        ])

        self.add_xpaths('cash', [
            '//us-gaap:CashCashEquivalentsAndFederalFundsSold',
            '//us-gaap:CashAndDueFromBanks',
            '//us-gaap:CashAndCashEquivalentsAtCarryingValue'
        ])

    def _get_symbol(self):
        try:
            filename = self.context['response'].url.split('/')[-1]
            return filename.split('-')[0].upper()
        except IndexError:
            return None

    def _get_doc_end_date(self):
        # the document end date could come from URL or document
        # in most cases, the date on URL is correct, but when the date on URL is not correct,
        # try to guess which one is more correct by checking the month
        date_str = self.context['response'].url.split('-')[-1].split('.')[0]
        date_on_url = datetime.strptime(date_str, '%Y%m%d')

        date_str = self.selector.select('//dei:DocumentPeriodEndDate/text()')[0].extract()
        date_in_doc = datetime.strptime(date_str, DATE_FORMAT)

        quarter_months = (3, 6, 9, 12)
        date = date_on_url
        if date_on_url.month not in quarter_months and date_in_doc.month in quarter_months:
            date = date_in_doc
        elif date_on_url.year != date_in_doc.year:
            # some documents have wrong year on URL, for instance,
            # on URL it's abc-20140630.xml, but it's 2013-06-30 in doc,
            # in this case, we count the year occurences in the document
            # to determine which one to use
            body = self.context['response'].body
            url_year_count = body.count(str(date_on_url.year))
            doc_year_count = body.count(str(date_in_doc.year))

            if doc_year_count > url_year_count:
                date = date_in_doc

        return date.strftime(DATE_FORMAT)

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
