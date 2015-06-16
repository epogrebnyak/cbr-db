import sys
sys.path.append('..')

import unittest
import cli_dates
from datetime import date

class CliDatesTest(unittest.TestCase):

    def test_get_date_fmt(self):
        test_strings = ['2005', '01.01.2005',  '1.1.2005', '1.2005', '2005-01', '2005-01-01']
        test_format = ['%Y', '%d.%m.%Y', '%d.%m.%Y', '%m.%Y', '%Y-%m', '%Y-%m-%d']
        target_date = date(2005, 1, 1)

        for string, target_format in zip(test_strings, test_format):
            date_, format_ = cli_dates.get_date(string, cli_dates.DATE_FORMATS)
            self.assertEqual(date_, target_date)
            self.assertEqual(format_, target_format)

    def test_get_date(self):
        self.assertEqual(cli_dates.get_date('1988', cli_dates.DATE_FORMATS)[0], date(1988, 1, 1))
        self.assertEqual(cli_dates.get_date('03.12.2015', cli_dates.DATE_FORMATS)[0], date(2015, 12, 3))
        self.assertEqual(cli_dates.get_date('2.2000', cli_dates.DATE_FORMATS)[0], date(2000, 2, 1))
        self.assertEqual(cli_dates.get_date('12.2030', cli_dates.DATE_FORMATS)[0], date(2030, 12, 1))
        self.assertEqual(cli_dates.get_date('2015-01-05', cli_dates.DATE_FORMATS)[0], date(2015, 1, 5))
        self.assertEqual(cli_dates.get_date('1977-12', cli_dates.DATE_FORMATS)[0], date(1977, 12, 1))

    def test_date_range(self): # yield was illegal name for test
        self.assertEqual(
            list(cli_dates.yield_date(date(2012, 3, 1), date(2012, 5, 1))),
            [date(2012, 3, 1), date(2012, 4, 1), date(2012, 5, 1)]
        )

        self.assertEqual(
            list(cli_dates.yield_date(date(1988, 11, 1), date(1989, 1, 1))),
            [date(1988, 11, 1), date(1988, 12, 1), date(1989, 1, 1)]
        )

    def test_shift_month_ahead(self):
        self.assertEqual(
            cli_dates.shift_month_ahead(date(2015, 5, 1)),
            date(2015, 6, 1)
        )

        self.assertEqual(
            cli_dates.shift_month_ahead(date(2012, 12, 1)),
            date(2013, 1, 1)
        )

        self.assertRaises(
            ValueError,
            cli_dates.shift_month_ahead,
            date(2013, 3, 31)
        )

    def test_get_date_range_from_command_line(self):
        args1 = {
            'pass': True,
            'form': '101',
            '<timestamp1>': '2005-01',
            '<timestamp2>': '2005-05',
            '--all-dates': False
        }

        self.assertEqual(
            list(cli_dates.get_date_range_from_command_line(args1)),
            ['2005-01-01', '2005-02-01', '2005-03-01', '2005-04-01', '2005-05-01']
        )

        args2 = {
            'pass': True,
            'form': '101',
            '<timestamp1>': '2004-10',
            '<timestamp2>': '2005-02',
            '--all-dates': False
        }

        self.assertEqual(
            list(cli_dates.get_date_range_from_command_line(args2)),
            ['2004-10-01', '2004-11-01', '2004-12-01', '2005-01-01', '2005-02-01']
        )

if __name__ == '__main__':
    unittest.main()