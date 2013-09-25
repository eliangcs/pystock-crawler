# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class DmozItem(Item):
    title = Field()
    link = Field()
    desc = Field()


class StockItem(Item):
    symbol = Field()
    key = Field()
    value = Field()
    date = Field()


class ReportItem(Item):
    # Trading symbol
    symbol = Field()

    # Quarterly (10-Q) or annual (10-K) report
    doc_type = Field()

    # Q1, Q2, Q3, or FY for annual report
    period_focus = Field()

    end_date = Field()

    revenues = Field()
    net_income = Field()

    eps_basic = Field()
    eps_diluted = Field()

    dividend = Field()

    assets = Field()
    debt = Field()
    equity = Field()
    cash = Field()
