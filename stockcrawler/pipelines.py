# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        sid = self._stringify(item)

        if sid in self.ids_seen:
            raise DropItem('Duplicate item found: %s' % item)

        self.ids_seen.add(sid)
        return item

    def _stringify(self, stock_item):
        return '%(symbol)s,%(key)s,%(value)s,%(date)s' % stock_item
