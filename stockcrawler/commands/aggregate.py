from scrapy.command import ScrapyCommand
from scrapy.exceptions import NotConfigured, UsageError
from scrapy.utils.misc import load_object

from stockcrawler.importers import parse


def _item_cmp(item1, item2):
    sym1 = item1['symbol']
    sym2 = item2['symbol']

    if sym1 > sym2:
        return 1
    elif sym1 < sym2:
        return -1

    date1 = item1['date']
    date2 = item2['date']

    if ':' in date1:
        date1 = date1.split(':')[-1]
    if ':' in date2:
        date2 = date2.split(':')[-1]

    if date1 > date2:
        return 1
    elif date1 < date2:
        return -1

    key1 = item1['key']
    key2 = item2['key']

    if key1 > key2:
        return 1
    elif key1 < key2:
        return -1

    return 0


class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return '[options] <input_file>'

    def short_desc(self):
        return 'Aggregate crawled stock data.'

    def add_options(self, parser):
        super(Command, self).add_options(parser)

        parser.add_option('-t', '--file-format', metavar='FORMAT', default=None,
            help='format of input and output files (default: file extension)')
        parser.add_option('-o', '--output', metavar='FILE',
            help='dump aggregated data into FILE (use - for stdout)')

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError()

        self.exporters = self._load_components('FEED_EXPORTERS')

        file_path = args[0]
        format = opts.file_format or file_path.split('.')[-1].lower()
        output_path = opts.output
        items = parse(file_path, format)
        items = sorted(items, _item_cmp)

        with open(output_path, 'wb') as output_file:
            exporter = self._get_exporter(format, output_file)
            exporter.fields_to_export = ['symbol', 'key', 'value', 'date']
            exporter.start_exporting()
            for item in items:
                exporter.export_item(item)
            exporter.finish_exporting()

    def _get_exporter(self, format, output_file):
        exporter_class = self.exporters.get(format)
        if exporter_class:
            return exporter_class(output_file)
        raise NotConfigured("Exporter '%s' is undefined" % format)

    def _load_components(self, setting_prefix):
        conf = dict(self.settings['%s_BASE' % setting_prefix])
        conf.update(self.settings[setting_prefix])
        d = {}
        for k, v in conf.items():
            try:
                d[k] = load_object(v)
            except NotConfigured:
                pass
        return d
