from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import XmlXPathSelector


def _find_namespace(xxs, name):
    name_re = name.replace('-', '\-')
    if not name_re.startswith('xmlns'):
        name_re = 'xmlns:' + name_re
    return xxs.re('%s=\"([^\"]+)\"' % name_re)[0]


def _register_namespace(xxs, name):
    ns = _find_namespace(xxs, name)
    xxs.register_namespace(name, ns)


def _register_namespaces(xxs):
    names = ('xmlns', 'xbrli', 'dei', 'us-gaap')
    for name in names:
        try:
            _register_namespace(xxs, name)
        except IndexError:
            pass


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
        _register_namespaces(xxs)

        f = open('E:/_debug.txt', 'a')

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

            f.write('%s: %s shares (class %s)\n' % (date, num_shares, stock_class))
        f.close()

        # print '--------------------------------------------'
        # print xxs.select('//dei:EntityCommonStockSharesOutstanding/text()').extract()
        # print xxs.select('//us-gaap:EarningsPerShareBasic/text()').extract()
