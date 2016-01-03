from datetime import date
import sys
sys.path.append('..')

import unittest
from cbr_db import cli_dates



class CliDatesTest(unittest.TestCase):

    def test_get_date_fmt(self):
        test_strings = ['2005', '01.01.2005',  '1.1.2005', '1.2005', '2005-01',
                        '2005-01-01', '2004Q4', '4q2004']
        test_format = ['%Y', '%d.%m.%Y', '%d.%m.%Y', '%m.%Y', '%Y-%m',
                       '%Y-%m-%d', 'quarter', 'quarter']
        target_date = date(2005, 1, 1)

        for string, target_format in zip(test_strings, test_format):
            date_, format_ = cli_dates.get_date(string)
            self.assertEqual(date_, target_date)
            self.assertEqual(format_, target_format)

    def test_get_date(self):
        self.assertEqual(cli_dates.get_date('1988')[0], date(1988, 1, 1))
        self.assertEqual(cli_dates.get_date('03.12.2015')[0], date(2015, 12, 3))
        self.assertEqual(cli_dates.get_date('2.2000')[0], date(2000, 2, 1))
        self.assertEqual(cli_dates.get_date('12.2030')[0], date(2030, 12, 1))
        self.assertEqual(cli_dates.get_date('2015-01-05')[0], date(2015, 1, 5))
        self.assertEqual(cli_dates.get_date('1977-12')[0], date(1977, 12, 1))
        self.assertEqual(cli_dates.get_date('1Q1988')[0], date(1988, 4, 1))
        self.assertEqual(cli_dates.get_date('2014q1')[0], date(2014, 4, 1))
        self.assertEqual(cli_dates.get_date('2014q2')[0], date(2014, 7, 1))
        self.assertEqual(cli_dates.get_date('2014q3')[0], date(2014, 10, 1))
        self.assertEqual(cli_dates.get_date('2014q4')[0], date(2015, 1, 1))

    def test_get_date_from_quarter_string(self):
        self.assertEqual(
            cli_dates.get_date_from_quarter_string("2000q1"),
            (date(2000, 4, 1), "quarter")
        )
        
        self.assertEqual(
            cli_dates.get_date_from_quarter_string("2000q4"),
            (date(2001, 1, 1), "quarter")
        )

    def test_get_last_quarter_month(self):
        for month in range(1, 4):        
            self.assertEqual(
                cli_dates.get_last_quarter_month(month), 1
            )
        
        for month in range(4, 7):        
            self.assertEqual(
                cli_dates.get_last_quarter_month(month), 4
            )
            
        for month in range(7, 10):        
            self.assertEqual(
                cli_dates.get_last_quarter_month(month), 7
            )
            
        for month in range(10, 13):        
            self.assertEqual(
                cli_dates.get_last_quarter_month(month), 10
            )
    
    def test_get_next_quarter_end_date(self):
        self.assertEqual(        
            cli_dates.get_next_quarter_end_date(date(2003, 1, 1)),
            date(2003, 1, 1)
        )
        
        for month in range(2, 5):        
            self.assertEqual(
                cli_dates.get_next_quarter_end_date(date(2003, month, 1)),
                date(2003, 4, 1)
            )
            
        for month in range(5, 8):        
            self.assertEqual(
                cli_dates.get_next_quarter_end_date(date(2003, month, 1)),
                date(2003, 7, 1)
            )
            
        for month in range(8, 11):        
            self.assertEqual(
                cli_dates.get_next_quarter_end_date(date(2003, month, 1)),
                date(2003, 10, 1)
            )
            
        for month in range(11, 12):        
            self.assertEqual(
                cli_dates.get_next_quarter_end_date(date(2003, month, 1)),
                date(2004, 1, 1)
            )

    def test_get_date_range_from_command_line_101(self):
        args1 = {
            'pass': True,
            '<form>': '101',
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
            '<form>': '101',
            '<timestamp1>': '2004-10',
            '<timestamp2>': '2005-02',
            '--all-dates': False
        }

        self.assertEqual(
            list(cli_dates.get_date_range_from_command_line(args2)),
            ['2004-10-01', '2004-11-01', '2004-12-01', '2005-01-01', '2005-02-01']
        )
        
    def test_get_date_range_from_command_line_102(self):
        args1 = {
            'pass': True,
            '<form>': '102',
            '<timestamp1>': '2004q3',
            '<timestamp2>': '1q2005',
            '--all-dates': False
        }

        self.assertEqual(
            list(cli_dates.get_date_range_from_command_line(args1)),
            ['2004-10-01', '2005-01-01', '2005-04-01']
        )
        
        args2 = {
            'pass': True,
            '<form>': '102',
            '<timestamp1>': '2004-02',
            '<timestamp2>': '2004-11',
            '--all-dates': False
        }

        self.assertEqual(
            list(cli_dates.get_date_range_from_command_line(args2)),
            ['2004-04-01', '2004-07-01', '2004-10-01']
        )
        
        args3 = {
            'pass': True,
            '<form>': '102',
            '<timestamp1>': '2013',
            '<timestamp2>': '2014',
            '--all-dates': False
        }

        self.assertEqual(
            list(cli_dates.get_date_range_from_command_line(args3)),
            ['2013-04-01', '2013-07-01', '2013-10-01', '2014-01-01',
             '2014-04-01', '2014-07-01', '2014-10-01', '2015-01-01']
        )
        
        args4 = {
            'pass': True,
            '<form>': '102',
            '<timestamp1>': '2013q1',
            '<timestamp2>': '4q2014',
            '--all-dates': False
        }

        self.assertEqual(
            list(cli_dates.get_date_range_from_command_line(args4)),
            ['2013-04-01', '2013-07-01', '2013-10-01', '2014-01-01',
             '2014-04-01', '2014-07-01', '2014-10-01', '2015-01-01']
        )

if __name__ == '__main__':
    unittest.main()
