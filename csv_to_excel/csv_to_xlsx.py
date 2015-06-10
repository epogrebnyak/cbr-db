"""Converts CSV to Excel files (xlsx)

Usage:
  csv_to_xlsx.py <from> <to> [--delimiter=<del>]
  csv_to_xlsx.py (-h | --help)

Options:
  -h --help     Show this screen.

"""
import csv
import xlsxwriter
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__, version='csv_to_xlsx 1.0')
    from_ = args['<from>']
    to = args['<to>']
    delimiter = args['--delimiter'] or '\t'

    with open(from_) as csv_f:
        reader = csv.reader(csv_f, delimiter=delimiter)
        workbook = xlsxwriter.Workbook(to)
        sheet = workbook.add_worksheet()

        for i, row in enumerate(reader):
            for j, val in enumerate(row):
                sheet.write(i, j, val)

        workbook.close()
