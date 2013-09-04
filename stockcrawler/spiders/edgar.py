from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import XmlXPathSelector


class URLGenerator(object):

    def __iter__(self):
        symbols = ('GOOG',)
        url = 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=10-Q&dateb=&owner=exclude&count=100'

        for symbol in symbols:
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
    start_urls = URLGenerator()

    rules = (
        Rule(SgmlLinkExtractor(allow=('/Archives/edgar/data/[^\"]+\-index\.htm',))),
        Rule(SgmlLinkExtractor(allow=('/Archives/edgar/data/[^\"]+\-\d{8}\.xml',)), callback='parse_10q'),
    )

    def parse_10q(self, response):
        xxs = XmlXPathSelector(response)
        try:
            dei_namespace = xxs.re('xmlns:dei=\"([^\"]+)\"')[0]
        except IndexError:
            return

        xxs.register_namespace('dei', dei_namespace)
        print '--------------------------------------------'
        print xxs.select('//dei:EntityCommonStockSharesOutstanding/text()').extract()
