import cStringIO
import re

from scrapy.spider import Spider

from pystock_crawler.items import SymbolItem


RE_SYMBOL = re.compile(r'^[A-Z]+$')


def generate_urls(exchanges):
    for exchange in exchanges:
        yield 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=%s&render=download' % exchange


class NasdaqSpider(Spider):

    name = 'nasdaq'
    allowed_domains = ['www.nasdaq.com']

    def __init__(self, **kwargs):
        super(NasdaqSpider, self).__init__(**kwargs)

        exchanges = kwargs.get('exchanges', '').split(',')
        self.start_urls = generate_urls(exchanges)

    def parse(self, response):
        try:
            file_like = cStringIO.StringIO(response.body)

            # Ignore first row
            file_like.next()

            for line in file_like:
                tokens = line.split(',')
                symbol = tokens[0].strip('"')
                if RE_SYMBOL.match(symbol):
                    name = tokens[1].strip('"')
                    yield SymbolItem(symbol=symbol, name=name)
        finally:
            file_like.close()
