#!/usr/bin/env python
import argparse
import csv


def parse_args():
    parser = argparse.ArgumentParser(description='Clean up the crawled CSV file.')
    parser.add_argument('input_file', metavar='INPUT_FILE', type=unicode,
                        help='Input CSV file')
    parser.add_argument('output_file', metavar='OUTPUT_FILE', type=unicode,
                        help='Output CSV file')
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


def item_cmp(a, b):
    cmp_sym = cmp(a['symbol'], b['symbol'])
    if cmp_sym == 0:
        return cmp(a['end_date'], b['end_date'])
    return cmp_sym


def sort_items(items):
    return sorted(items, cmp=item_cmp)


def dict_to_list(a, keys):
    result = []
    for k in keys:
        result.append(a[k])
    return result


def write_csv(items, file_path):
    headers = ['symbol', 'doc_type', 'amend', 'end_date', 'period_focus',
               'revenues', 'net_income', 'eps_basic', 'eps_diluted', 'dividend',
               'assets', 'cash', 'equity']

    with open(file_path, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for item in items:
            row = dict_to_list(item, headers)
            writer.writerow(row)


def main():
    args = parse_args()
    items = parse_csv(args.input_file)
    items = sort_items(items)
    write_csv(items, args.output_file)


if __name__ == '__main__':
    main()
