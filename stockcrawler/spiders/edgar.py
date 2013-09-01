from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider


class URLGenerator(object):

    def __iter__(self):
        symbols = ('GOOG', 'APPL', 'FB')
        url = 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=10-Q&dateb=&owner=exclude&count=100'

        for symbol in symbols:
            yield (url % symbol)


class EdgarSpider(BaseSpider):

    name = 'edgar'
    allowed_domains = ['sec.gov']
    start_urls = URLGenerator()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        doc_urls = hxs.select('//a[starts-with(@href, "/Archives/edgar/data/")]/@href').extract()
        for url in doc_urls:
            print 'URL: %s' % url
