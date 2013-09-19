import csv

from stockcrawler.items import StockItem


class CSVImporter(object):

    def parse(self, file_obj):
        reader = csv.reader(file_obj)
        fields = reader.next()

        items = []

        for row in reader:
            item = StockItem()
            for i in xrange(0, len(row)):
                field = fields[i]
                item[field] = row[i]
            items.append(item)

        return items


def parse(file_path, format=None):
    format = format or file_path.split('.')[-1].lower()

    importer_classes = {
        'csv': CSVImporter
    }
    importer_class = importer_classes.get(format)
    if not importer_class:
        raise NotImplementedError("Importer '%s' not implemented" % format)

    importer = importer_class()

    with open(file_path) as file_obj:
        return importer.parse(file_obj)
