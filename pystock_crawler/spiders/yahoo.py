import cStringIO
import os
import re

from datetime import datetime
from scrapy.spider import Spider

from pystock_crawler import utils
from pystock_crawler.items import PriceItem


def parse_date(date_str):
    if date_str:
        date = datetime.strptime(date_str, '%Y%m%d')
        return date.year, date.month - 1, date.day
    return '', '', ''


def make_url(symbol, start_date=None, end_date=None):
    url = ('http://ichart.finance.yahoo.com/table.csv?'
           's=%(symbol)s&d=%(end_month)s&e=%(end_day)s&f=%(end_year)s&g=d&'
           'a=%(start_month)s&b=%(start_day)s&c=%(start_year)s&ignore=.csv')

    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    return url % {
        'symbol': symbol,
        'start_year': start_date[0],
        'start_month': start_date[1],
        'start_day': start_date[2],
        'end_year': end_date[0],
        'end_month': end_date[1],
        'end_day': end_date[2]
    }


def generate_urls(symbols, start_date=None, end_date=None):
    for symbol in symbols:
        yield make_url(symbol, start_date, end_date)


class YahooSpider(Spider):

    name = 'yahoo'
    allowed_domains = ['finance.yahoo.com']

    def __init__(self, **kwargs):
        super(YahooSpider, self).__init__(**kwargs)

        symbols_arg = kwargs.get('symbols')
        start_date = kwargs.get('startdate', '')
        end_date = kwargs.get('enddate', '')

        utils.check_date_arg(start_date, 'startdate')
        utils.check_date_arg(end_date, 'enddate')

        if symbols_arg:
            if os.path.exists(symbols_arg):
                # get symbols from a text file
                symbols = utils.load_symbols(symbols_arg)
            else:
                # inline symbols in command
                symbols = symbols_arg.split(',')
            self.start_urls = generate_urls(symbols, start_date, end_date)
        else:
            self.start_urls = []

    def parse(self, response):
        symbol = self._get_symbol_from_url(response.url)
        try:
            file_like = cStringIO.StringIO(response.body)
            rows = utils.parse_csv(file_like)
            for row in rows:
                item = PriceItem(symbol=symbol)
                for k, v in row.iteritems():
                    item[k.replace(' ', '_').lower()] = v
                yield item
        finally:
            file_like.close()

    def _get_symbol_from_url(self, url):
        match = re.search(r'[\?&]s=([^&]*)', url)
        if match:
            return match.group(1)
        return ''
