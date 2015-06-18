import sys
sys.path.append('..')

import unittest
from datetime import date
import date_engine

class DateEngineTest(unittest.TestCase):

    def test_shift_month_ahead(self):
        self.assertEqual(
            date_engine.shift_month_ahead(date(2015, 5, 1)),
            date(2015, 6, 1)
        )

        self.assertEqual(
            date_engine.shift_month_ahead(date(2012, 12, 1)),
            date(2013, 1, 1)
        )

        self.assertRaises(
            ValueError,
            date_engine.shift_month_ahead,
            date(2013, 3, 31)
        )

    def test_get_date_range(self):
        self.assertEqual(
            date_engine.get_date_range(date(2012, 3, 1), date(2012, 5, 1)),
            [date(2012, 3, 1), date(2012, 4, 1), date(2012, 5, 1)]
        )

        self.assertEqual(
            date_engine.get_date_range(date(1988, 11, 1), date(1989, 1, 1)),
            [date(1988, 11, 1), date(1988, 12, 1), date(1989, 1, 1)]
        )

    def test_zero_padded_month(self):
        self.assertEqual(
            date_engine.zero_padded_month(5),
            "05"
        )

        self.assertEqual(
            date_engine.zero_padded_month(11),
            "11"
        )

    def test_datetime2iso(self):
        self.assertEqual(
            date_engine.date2iso(date(1988, 1, 1)),
            '1988-01-01'
        )

        self.assertEqual(
            date_engine.date2iso(date(2015, 5, 23)),
            '2015-05-23'
        )

    def test_iso2date(self):
        self.assertEqual(
            date_engine.iso2date('1988-01-01'),
            date(1988, 1, 1)
        )

        self.assertEqual(
            date_engine.iso2date('2015-05-23'),
            date(2015, 5, 23)
        )

    def test_date2timestamp(self):
        self.assertEqual(
            date_engine.date2timestamp(101, date(2014, 5, 3)),
            '042014'
        )

        self.assertEqual(
            date_engine.date2timestamp('101', date(2014, 1, 5)),
            '122013'
        )

    def test_isodate2timestamp(self):
        self.assertEqual(
            date_engine.isodate2timestamp(101, '2014-05-03'),
            '042014'
        )

        self.assertEqual(
            date_engine.isodate2timestamp('101', '2014-01-05'),
            '122013'
        )

if __name__ == '__main__':
    unittest.main()