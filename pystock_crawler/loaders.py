import re

from datetime import datetime, timedelta
from scrapy import log
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Compose, MapCompose, TakeFirst
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import flatten

from pystock_crawler.items import ReportItem


DATE_FORMAT = '%Y-%m-%d'

MAX_PER_SHARE_VALUE = 1000.0

# If number of characters of response body exceeds this value,
# remove some useless text defined by RE_XML_GARBAGE to reduce memory usage
THRESHOLD_TO_CLEAN = 20000000

# Used to get rid of "<tag>LONG STRING...</tag>"
RE_XML_GARBAGE = re.compile(r'>([^<]{100,})<')


class IntermediateValue(object):
    '''
    Intermediate data that serves as output of input processors, i.e., input
    of output processors. "Intermediate" is shorten as "imd" in later naming.

    '''
    def __init__(self, local_name, value, text, context, node=None, start_date=None,
                 end_date=None, instant=None):
        self.local_name = local_name
        self.value = value
        self.text = text
        self.context = context
        self.node = node
        self.start_date = start_date
        self.end_date = end_date
        self.instant = instant

    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        return 0

    def __repr__(self):
        context_id = None
        if self.context:
            context_id = self.context.xpath('@id')[0].extract()
        return '(%s, %s, %s)' % (self.local_name, self.value, context_id)

    def is_member(self):
        return is_member(self.context)


class ExtractText(object):

    def __call__(self, value):
        if hasattr(value, 'select'):
            try:
                return value.xpath('./text()')[0].extract()
            except IndexError:
                return ''
        return unicode(value)


class MatchEndDate(object):

    def __init__(self, data_type=str, ignore_date_range=False):
        self.data_type = data_type
        self.ignore_date_range = ignore_date_range

    def __call__(self, value, loader_context):
        if not hasattr(value, 'select'):
            return IntermediateValue('', 0.0, '0', None)

        doc_end_date_str = loader_context['end_date']
        doc_type = loader_context['doc_type']
        selector = loader_context['selector']

        context_id = value.xpath('@contextRef')[0].extract()
        try:
            context = selector.xpath('//*[@id="%s"]' % context_id)[0]
        except IndexError:
            try:
                url = loader_context['response'].url
            except KeyError:
                url = None
            log.msg(u'Cannot find context: %s in %s' % (context_id, url), log.WARNING)
            return None

        date = instant = start_date = end_date = None
        try:
            instant = context.xpath('.//*[local-name()="instant"]/text()')[0].extract().strip()
        except (IndexError, ValueError):
            try:
                end_date_str = context.xpath('.//*[local-name()="endDate"]/text()')[0].extract().strip()
                end_date = datetime.strptime(end_date_str, DATE_FORMAT)

                start_date_str = context.xpath('.//*[local-name()="startDate"]/text()')[0].extract().strip()
                start_date = datetime.strptime(start_date_str, DATE_FORMAT)

                if self.ignore_date_range or date_range_matches_doc_type(doc_type, start_date, end_date):
                    date = end_date
            except (IndexError, ValueError):
                pass
        else:
            try:
                instant = datetime.strptime(instant, DATE_FORMAT)
            except ValueError:
                pass
            else:
                date = instant

        if date:
            doc_end_date = datetime.strptime(doc_end_date_str, DATE_FORMAT)
            delta_days = (doc_end_date - date).days
            if abs(delta_days) < 30:
                try:
                    text = value.xpath('./text()')[0].extract()
                    val = self.data_type(text)
                except (IndexError, ValueError):
                    pass
                else:
                    local_name = value.xpath('local-name()')[0].extract()
                    return IntermediateValue(
                        local_name, val, text, context, value,
                        start_date=start_date, end_date=end_date, instant=instant)

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
            return imd_sum(members)

        if imd_values:
            return self.second_func(non_members)
        return None


def date_range_matches_doc_type(doc_type, start_date, end_date):
    delta_days = (end_date - start_date).days
    return ((doc_type == '10-Q' and delta_days < 120 and delta_days > 60) or
            (doc_type == '10-K' and delta_days < 380 and delta_days > 350))


def get_amend(values):
    if values:
        return values[0]
    return False


def get_symbol(values):
    if values:
        symbols = map(lambda s: s.strip(), values[0].split(','))
        return '/'.join(symbols)
    return False


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


def imd_sum(imd_values):
    return sum([v.value for v in imd_values])


def imd_get_revenues(imd_values):
    interest_elems = filter(lambda v: 'interest' in v.local_name.lower(), imd_values)
    if len(interest_elems) == len(imd_values):
        # HACK: An exceptional case for BBT
        # Revenues = InterestIncome + NoninterestIncome
        return imd_sum(imd_values)

    return imd_max(imd_values)


def imd_get_net_income(imd_values):
    return imd_min(imd_values)


def imd_get_op_income(imd_values):
    imd_values = filter(lambda v: memberness(v.context) < 2, imd_values)
    return imd_min(imd_values)


def imd_get_cash_flow(imd_values, loader_context):
    if len(imd_values) == 1:
        return imd_values[0].value

    doc_type = loader_context['doc_type']

    within_date_range = []
    for imd_value in imd_values:
        if imd_value.start_date and imd_value.end_date:
            if date_range_matches_doc_type(doc_type, imd_value.start_date, imd_value.end_date):
                within_date_range.append(imd_value)

    if within_date_range:
        return imd_max(within_date_range)

    return imd_max(imd_values)


def imd_get_per_share_value(imd_values):
    if not imd_values:
        return None

    v = imd_values[0]
    value = v.value
    if abs(value) > MAX_PER_SHARE_VALUE:
        try:
            decimals = int(v.node.xpath('@decimals')[0].extract())
        except (AttributeError, IndexError, ValueError):
            return None
        else:
            # HACK: some of LTD's reports have unreasonablely large per share value, such as
            # 320000 EPS (and it should be 0.32), so use decimals attribute to scale it down,
            # note that this is NOT a correct way to interpret decimals attribute
            value *= pow(10, decimals - 2)
    return value if abs(value) <= MAX_PER_SHARE_VALUE else None


def imd_get_equity(imd_values):
    if not imd_values:
        return None

    values = filter(lambda v: v.local_name == 'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest', imd_values)
    if values:
        return values[0].value

    values = filter(lambda v: v.local_name == 'StockholdersEquity', imd_values)
    if values:
        return values[0].value

    return imd_values[0].value


def imd_filter_member(imd_values):
    if imd_values:
        with_memberness = [(v, memberness(v.context)) for v in imd_values]
        with_memberness = sorted(with_memberness, cmp=lambda a, b: a[1] - b[1])

        m0 = with_memberness[0][1]
        non_members = []

        for v in with_memberness:
            if v[1] == m0:
                non_members.append(v[0])

        return non_members

    return imd_values


def imd_mult(imd_values):
    for v in imd_values:
        try:
            node_id = v.node.xpath('@id')[0].extract().lower()
        except (AttributeError, IndexError):
            pass
        else:
            # HACK: some of LUV's reports have unreasonablely small numbers such as
            # 4136 in revenues which should be 4136 millions, this hack uses id attribute
            # to determine if it should be scaled up
            if 'inmillions' in node_id and abs(v.value) < 100000.0:
                v.value *= 1000000.0
            elif 'inthousands' in node_id and abs(v.value) < 100000000.0:
                v.value *= 1000.0
    return imd_values


def memberness(context):
    '''The likelihood that the context is a "member".'''
    if context:
        texts = context.xpath('.//*[local-name()="explicitMember"]/text()').extract()
        text = str(texts).lower()

        if len(texts) > 1:
            return 2
        elif 'country' in text:
            return 2
        elif 'member' not in text:
            return 0
        elif 'successor' in text:
            # 'SuccessorMember' is a rare case that shouldn't be treated as member
            return 1
        elif 'parent' in text:
            return 2
    return 3


def is_member(context):
    if context:
        texts = context.xpath('.//*[local-name()="explicitMember"]/text()').extract()
        text = str(texts).lower()

        # 'SuccessorMember' is a rare case that shouldn't be treated as member
        if 'member' not in text or 'successor' in text or 'parent' in text:
            return False
    return True


def str_to_bool(value):
    if hasattr(value, 'lower'):
        value = value.lower()
        return bool(value) and value != 'false' and value != '0'
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


class XmlXPathItemLoader(ItemLoader):

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
        return flatten([self.selector.xpath(xpath) for xpath in xpaths])


class ReportItemLoader(XmlXPathItemLoader):

    default_item_class = ReportItem
    default_output_processor = TakeFirst()

    symbol_in = MapCompose(ExtractText(), unicode.upper)
    symbol_out = Compose(get_symbol)

    amend_in = MapCompose(ExtractText(), str_to_bool)
    amend_out = Compose(get_amend)

    period_focus_in = MapCompose(ExtractText(), unicode.upper)
    period_focus_out = TakeFirst()

    revenues_in = MapCompose(MatchEndDate(float))
    revenues_out = Compose(imd_filter_member, imd_mult, ImdSumMembersOr(imd_get_revenues))

    net_income_in = MapCompose(MatchEndDate(float))
    net_income_out = Compose(imd_filter_member, imd_mult, imd_get_net_income)

    op_income_in = MapCompose(MatchEndDate(float))
    op_income_out = Compose(imd_filter_member, imd_mult, imd_get_op_income)

    eps_basic_in = MapCompose(MatchEndDate(float))
    eps_basic_out = Compose(ImdSumMembersOr(imd_get_per_share_value), lambda x: x if x < MAX_PER_SHARE_VALUE else None)

    eps_diluted_in = MapCompose(MatchEndDate(float))
    eps_diluted_out = Compose(ImdSumMembersOr(imd_get_per_share_value), lambda x: x if x < MAX_PER_SHARE_VALUE else None)

    dividend_in = MapCompose(MatchEndDate(float))
    dividend_out = Compose(imd_get_per_share_value, lambda x: x if x < MAX_PER_SHARE_VALUE and x > 0.0 else 0.0)

    assets_in = MapCompose(MatchEndDate(float))
    assets_out = Compose(imd_filter_member, imd_mult, imd_max)

    cur_assets_in = MapCompose(MatchEndDate(float))
    cur_assets_out = Compose(imd_filter_member, imd_mult, imd_max)

    cur_liab_in = MapCompose(MatchEndDate(float))
    cur_liab_out = Compose(imd_filter_member, imd_mult, imd_max)

    equity_in = MapCompose(MatchEndDate(float))
    equity_out = Compose(imd_filter_member, imd_mult, imd_get_equity)

    cash_in = MapCompose(MatchEndDate(float))
    cash_out = Compose(imd_filter_member, imd_mult, imd_max)

    cash_flow_op_in = MapCompose(MatchEndDate(float, True))
    cash_flow_op_out = Compose(imd_filter_member, imd_mult, imd_get_cash_flow)

    cash_flow_inv_in = MapCompose(MatchEndDate(float, True))
    cash_flow_inv_out = Compose(imd_filter_member, imd_mult, imd_get_cash_flow)

    cash_flow_fin_in = MapCompose(MatchEndDate(float, True))
    cash_flow_fin_out = Compose(imd_filter_member, imd_mult, imd_get_cash_flow)

    def __init__(self, *args, **kwargs):
        response = kwargs.get('response')
        if len(response.body) > THRESHOLD_TO_CLEAN:
            # Remove some useless text to reduce memory usage
            body, __ = RE_XML_GARBAGE.subn(lambda m: '><', response.body)
            response = response.replace(body=body)
            kwargs['response'] = response

        super(ReportItemLoader, self).__init__(*args, **kwargs)

        symbol = self._get_symbol()
        end_date = self._get_doc_end_date()
        fiscal_year = self._get_doc_fiscal_year()
        doc_type = self._get_doc_type()

        # ignore document that is not 10-Q or 10-K
        if not (doc_type and doc_type.split('/')[0] in ('10-Q', '10-K')):
            return

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

        if doc_type == '10-K':
            period_focus = 'FY'
        else:
            period_focus = self._get_period_focus(end_date)

        if not fiscal_year and period_focus:
            fiscal_year = self._guess_fiscal_year(end_date, period_focus)

        self.add_value('period_focus', period_focus)
        self.add_value('fiscal_year', fiscal_year)
        self.add_value('end_date', end_date)
        self.add_value('doc_type', doc_type)

        self.add_xpaths('revenues', [
            '//us-gaap:SalesRevenueNet',
            '//us-gaap:Revenues',
            '//us-gaap:SalesRevenueGoodsNet',
            '//us-gaap:SalesRevenueServicesNet',
            '//us-gaap:RealEstateRevenueNet',
            '//*[local-name()="NetRevenuesIncludingNetInterestIncome"]',
            '//*[contains(local-name(), "TotalRevenues") and contains(local-name(), "After")]',
            '//*[contains(local-name(), "TotalRevenues")]',
            '//*[local-name()="InterestAndDividendIncomeOperating" or local-name()="NoninterestIncome"]',
            '//*[contains(local-name(), "Revenue")]'
        ])
        self.add_xpath('revenues', '//us-gaap:FinancialServicesRevenue')

        self.add_xpaths('net_income', [
            '//*[contains(local-name(), "NetLossIncome") and contains(local-name(), "Corporation")]',
            '//*[local-name()="NetIncomeLossAvailableToCommonStockholdersBasic" or local-name()="NetIncomeLoss"]',
            '//us-gaap:ProfitLoss',
            '//us-gaap:IncomeLossFromContinuingOperations',
            '//*[contains(local-name(), "IncomeLossFromContinuingOperations") and not(contains(local-name(), "Per"))]',
            '//*[contains(local-name(), "NetIncomeLoss")]',
            '//*[starts-with(local-name(), "NetIncomeAttributableTo")]'
        ])

        self.add_xpaths('op_income', [
            '//us-gaap:OperatingIncomeLoss'
        ])

        self.add_xpaths('eps_basic', [
            '//us-gaap:EarningsPerShareBasic',
            '//us-gaap:IncomeLossFromContinuingOperationsPerBasicShare',
            '//us-gaap:IncomeLossFromContinuingOperationsPerBasicAndDilutedShare',
            '//*[contains(local-name(), "NetIncomeLoss") and contains(local-name(), "Per") and contains(local-name(), "Common")]',
            '//*[contains(local-name(), "Earnings") and contains(local-name(), "Per") and contains(local-name(), "Basic")]',
            '//*[local-name()="IncomePerShareFromContinuingOperationsAvailableToCompanyStockholdersBasicAndDiluted"]',
            '//*[contains(local-name(), "NetLossPerShare")]',
            '//*[contains(local-name(), "NetIncome") and contains(local-name(), "Per") and contains(local-name(), "Basic")]',
            '//*[local-name()="BasicEarningsAttributableToStockholdersPerCommonShare"]',
            '//*[local-name()="Earningspersharebasicanddiluted"]',
            '//*[contains(local-name(), "PerCommonShareBasicAndDiluted")]',
            '//*[local-name()="NetIncomeLossAttributableToCommonStockholdersBasicAndDiluted"]',
            '//us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic',
            '//*[local-name()="NetIncomeLossEPS"]',
            '//*[local-name()="NetLoss"]'
        ])

        self.add_xpaths('eps_diluted', [
            '//us-gaap:EarningsPerShareDiluted',
            '//us-gaap:IncomeLossFromContinuingOperationsPerDilutedShare',
            '//us-gaap:IncomeLossFromContinuingOperationsPerBasicAndDilutedShare',
            '//*[contains(local-name(), "Earnings") and contains(local-name(), "Per") and contains(local-name(), "Diluted")]',
            '//*[local-name()="IncomePerShareFromContinuingOperationsAvailableToCompanyStockholdersBasicAndDiluted"]',
            '//*[contains(local-name(), "NetLossPerShare")]',
            '//*[contains(local-name(), "NetIncome") and contains(local-name(), "Per") and contains(local-name(), "Diluted")]',
            '//*[local-name()="DilutedEarningsAttributableToStockholdersPerCommonShare"]',
            '//us-gaap:NetIncomeLossAvailableToCommonStockholdersDiluted',
            '//*[contains(local-name(), "PerCommonShareBasicAndDiluted")]',
            '//*[local-name()="NetIncomeLossAttributableToCommonStockholdersBasicAndDiluted"]',
            '//us-gaap:EarningsPerShareBasic',
            '//*[local-name()="NetIncomeLossEPS"]',
            '//*[local-name()="NetLoss"]'
        ])

        self.add_xpaths('dividend', [
            '//us-gaap:CommonStockDividendsPerShareDeclared',
            '//us-gaap:CommonStockDividendsPerShareCashPaid'
        ])

        # if dividend isn't found in doc, assume it's 0
        self.add_value('dividend', 0.0)

        self.add_xpaths('assets', [
            '//us-gaap:Assets',
            '//us-gaap:AssetsNet',
            '//us-gaap:LiabilitiesAndStockholdersEquity'
        ])

        self.add_xpaths('cur_assets', [
            '//us-gaap:AssetsCurrent'
        ])

        self.add_xpaths('cur_liab', [
            '//us-gaap:LiabilitiesCurrent'
        ])

        self.add_xpaths('equity', [
            '//*[local-name()="StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest" or local-name()="StockholdersEquity"]',
            '//*[local-name()="TotalCommonShareholdersEquity"]',
            '//*[local-name()="CommonShareholdersEquity"]',
            '//*[local-name()="CommonStockEquity"]',
            '//*[local-name()="TotalEquity"]',
            '//us-gaap:RetainedEarningsAccumulatedDeficit',
            '//*[contains(local-name(), "MembersEquityIncludingPortionAttributableToNoncontrollingInterest")]',
            '//us-gaap:CapitalizationLongtermDebtAndEquity',
            '//*[local-name()="TotalCapitalization"]'
        ])

        self.add_xpaths('cash', [
            '//us-gaap:CashCashEquivalentsAndFederalFundsSold',
            '//us-gaap:CashAndDueFromBanks',
            '//us-gaap:CashAndCashEquivalentsAtCarryingValue',
            '//us-gaap:Cash',
            '//*[local-name()="CashAndCashEquivalents"]',
            '//*[contains(local-name(), "CarryingValueOfCashAndCashEquivalents")]',
            '//*[contains(local-name(), "CashCashEquivalents")]',
            '//*[contains(local-name(), "CashAndCashEquivalents")]'
        ])

        self.add_xpaths('cash_flow_op', [
            '//us-gaap:NetCashProvidedByUsedInOperatingActivities',
            '//us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations'
        ])

        self.add_xpaths('cash_flow_inv', [
            '//us-gaap:NetCashProvidedByUsedInInvestingActivities',
            '//us-gaap:NetCashProvidedByUsedInInvestingActivitiesContinuingOperations'
        ])

        self.add_xpaths('cash_flow_fin', [
            '//us-gaap:NetCashProvidedByUsedInFinancingActivities',
            '//us-gaap:NetCashProvidedByUsedInFinancingActivitiesContinuingOperations'
        ])

    def _get_symbol(self):
        try:
            filename = self.context['response'].url.split('/')[-1]
            return filename.split('-')[0].upper()
        except IndexError:
            return None

    def _get_doc_fiscal_year(self):
        try:
            fiscal_year = self.selector.xpath('//dei:DocumentFiscalYearFocus/text()')[0].extract()
            return int(fiscal_year)
        except (IndexError, ValueError):
            return None

    def _guess_fiscal_year(self, end_date, period_focus):
        # Guess fiscal_year based on document end_date and period_focus
        date = datetime.strptime(end_date, DATE_FORMAT)
        month_ranges = {
            'Q1': (2, 3, 4),
            'Q2': (5, 6, 7),
            'Q3': (8, 9, 10),
            'FY': (11, 12, 1)
        }
        month_range = month_ranges.get(period_focus)

        # Case 1: release Q1 around March, Q2 around June, ...
        # This is what most companies do
        if date.month in month_range:
            if period_focus == 'FY' and date.month == 1:
                return date.year - 1
            return date.year

        # How many days left before 10-K's release?
        days_left_table = {
            'Q1': 270,
            'Q2': 180,
            'Q3': 90,
            'FY': 0
        }
        days_left = days_left_table.get(period_focus)

        # Other cases, assume end_date.year of its FY report equals to
        # its fiscal_year
        if days_left is not None:
            fy_date = date + timedelta(days=days_left)
            return fy_date.year

        return None

    def _get_doc_end_date(self):
        # the document end date could come from URL or document content
        # we need to guess which one is correct
        url_date_str = self.context['response'].url.split('-')[-1].split('.')[0]
        url_date = datetime.strptime(url_date_str, '%Y%m%d')
        url_date_str = url_date.strftime(DATE_FORMAT)

        try:
            doc_date_str = self.selector.xpath('//dei:DocumentPeriodEndDate/text()')[0].extract()
            doc_date = datetime.strptime(doc_date_str, DATE_FORMAT)
        except (IndexError, ValueError):
            return url_date.strftime(DATE_FORMAT)

        context_date_strs = set(self.selector.xpath('//*[local-name()="context"]//*[local-name()="endDate"]/text()').extract())

        date = url_date
        if doc_date_str in context_date_strs:
            date = doc_date

        return date.strftime(DATE_FORMAT)

    def _get_doc_type(self):
        try:
            return self.selector.xpath('//dei:DocumentType/text()')[0].extract().upper()
        except (IndexError, ValueError):
            return None

    def _get_period_focus(self, doc_end_date):
        try:
            return self.selector.xpath('//dei:DocumentFiscalPeriodFocus/text()')[0].extract().upper()
        except IndexError:
            pass

        try:
            doc_yr = doc_end_date.split('-')[0]
            yr_end_date = self.selector.xpath('//dei:CurrentFiscalYearEndDate/text()')[0].extract()
            yr_end_date = yr_end_date.replace('--', doc_yr + '-')
        except IndexError:
            return None

        doc_end_date = datetime.strptime(doc_end_date, '%Y-%m-%d')
        yr_end_date = datetime.strptime(yr_end_date, '%Y-%m-%d')
        delta_days = (yr_end_date - doc_end_date).days

        if delta_days > -45 and delta_days < 45:
            return 'FY'
        elif (delta_days <= -45 and delta_days > -135) or delta_days > 225:
            return 'Q1'
        elif (delta_days <= -135 and delta_days > -225) or (delta_days > 135 and delta_days <= 225):
            return 'Q2'
        elif delta_days <= -225 or (delta_days > 45 and delta_days <= 135):
            return 'Q3'

        return 'FY'
