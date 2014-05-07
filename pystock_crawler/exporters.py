from scrapy.conf import settings
from scrapy.contrib.exporter import BaseItemExporter, CsvItemExporter


class CsvItemExporter2(CsvItemExporter):
    '''
    The standard CsvItemExporter class does not pass the kwargs through to the
    CSV writer, resulting in EXPORT_FIELDS and EXPORT_ENCODING being ignored
    (EXPORT_EMPTY is not used by CSV).

    http://stackoverflow.com/questions/6943778/python-scrapy-how-to-get-csvitemexporter-to-write-columns-in-a-specific-order

    '''
    def __init__(self, *args, **kwargs):
        kwargs['fields_to_export'] = settings.getlist('EXPORT_FIELDS') or None
        kwargs['encoding'] = settings.get('EXPORT_ENCODING', 'utf-8')

        super(CsvItemExporter2, self).__init__(*args, **kwargs)

    def _write_headers_and_set_fields_to_export(self, item):
        # HACK: Override this private method to filter fields that are in
        # fields_to_export but not in item
        if self.include_headers_line:
            item_fields = item.fields.keys()
            if self.fields_to_export:
                self.fields_to_export = filter(lambda a: a in item_fields, self.fields_to_export)
            else:
                self.fields_to_export = item_fields
            self.csv_writer.writerow(self.fields_to_export)


class SymbolListExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file

    def export_item(self, item):
        self.file.write('%s\t%s\n' % (item['symbol'], item['name']))
