from scrapy.http import TextResponse

from pystock_crawler.spiders.nasdaq import NasdaqSpider
from pystock_crawler.tests.base import TestCaseBase


class NasdaqSpiderTest(TestCaseBase):

    def test_parse(self):
        spider = NasdaqSpider()

        body = ('"Symbol","Name","Doesnt Matter",\n'
                '"DDD","3D Systems Corporation","50.5",\n'
                '"VNO","Vornado Realty Trust","103.5",\n'
                '"VNO^G","Vornado Realty Trust","25.21",\n'
                '"WBS","Webster Financial Corporation","29.71",\n'
                '"WBS/WS","Webster Financial Corporation","13.07",\n'
                '"AAA-A","Some Fake Company","1234.0",')
        response = TextResponse('http://www.nasdaq.com/dummy_url', body=body)
        items = list(spider.parse(response))

        self.assertEqual(len(items), 3)
        self.assert_item(items[0], {
            'symbol': 'DDD',
            'name': '3D Systems Corporation'
        })
        self.assert_item(items[1], {
            'symbol': 'VNO',
            'name': 'Vornado Realty Trust'
        })
        self.assert_item(items[2], {
            'symbol': 'WBS',
            'name': 'Webster Financial Corporation'
        })
