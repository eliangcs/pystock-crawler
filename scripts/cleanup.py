#!/usr/bin/env python
import argparse
import csv


def parse_args():
    parser = argparse.ArgumentParser(description='Clean up the crawled CSV file.')
    parser.add_argument('data_type', metavar='DATA_TYPE', type=unicode,
                        choices=('reports', 'prices'),
                        help="what's in the input file, 'reports' or 'prices'?")
    parser.add_argument('input_file', metavar='INPUT_FILE', type=unicode,
                        help='input CSV file')
    parser.add_argument('-o', metavar='OUTPUT_FILE', type=unicode,
                        help='output CSV file, overwrite INPUT_FILE if not specified')
    return parser.parse_args()


def parse_csv(file_path):
    with open(file_path, 'rb') as f:
        reader = csv.reader(f)
        headers = reader.next()

        for row in reader:
            item = {}
            for i, value in enumerate(row):
                header = headers[i]
                item[header] = value
            yield item


def item_cmp_report(a, b):
    cmp_sym = cmp(a['symbol'], b['symbol'])
    if cmp_sym == 0:
        return cmp(a['end_date'], b['end_date'])
    return cmp_sym


def item_cmp_price(a, b):
    cmp_sym = cmp(a['symbol'], b['symbol'])
    if cmp_sym == 0:
        return cmp(a['date'], b['date'])
    return cmp_sym


def dict_to_list(a, keys):
    result = []
    for k in keys:
        result.append(a[k])
    return result


def write_csv(items, file_path, headers):
    with open(file_path, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for item in items:
            row = dict_to_list(item, headers)
            writer.writerow(row)


CMPS = {
    'reports': item_cmp_report,
    'prices': item_cmp_price
}

HEADERS = {
    'reports': (
        'symbol', 'doc_type', 'amend', 'end_date', 'period_focus',
        'revenues', 'net_income', 'eps_basic', 'eps_diluted', 'dividend',
        'assets', 'cash', 'equity'
    ),
    'prices': (
        'symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close'
    )
}


def main():
    args = parse_args()
    headers = HEADERS[args.data_type]
    items = parse_csv(args.input_file)
    items = sorted(items, cmp=CMPS[args.data_type])
    write_csv(items, args.o or args.input_file, headers)


if __name__ == '__main__':
    main()
