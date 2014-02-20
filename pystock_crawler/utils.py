import csv

from datetime import datetime


def check_date_arg(value, arg_name=None):
    if value:
        try:
            if len(value) != 8:
                raise ValueError
            datetime.strptime(value, '%Y%m%d')
        except ValueError:
            raise ValueError("Option '%s' must be in YYYYMMDD format, input is '%s'" % (arg_name, value))


def load_symbols(file_path):
    symbols = []
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                symbol = line.split()[0]
                symbols.append(symbol)
    return symbols


def parse_csv(file_like):
    reader = csv.reader(file_like)
    headers = reader.next()
    for row in reader:
        item = {}
        for i, value in enumerate(row):
            header = headers[i]
            item[header] = value
        yield item
