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

    def test_get_isodate_list(self):
        self.assertEqual(
            date_engine.get_isodate_list('2012-03-01', '2012-05-01'),
            ['2012-03-01', '2012-04-01', '2012-05-01']
        )

        self.assertEqual(
            date_engine.get_isodate_list('1988-11-01', '1989-01-01'),
            ['1988-11-01', '1988-12-01', '1989-01-01']
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

    def test_timestamp2date(self):
        self.assertEqual(
            date_engine.timestamp2date(2015, 5),
            date(2015, 6, 1)
        )

        self.assertEqual(
            date_engine.timestamp2date(1992, 12),
            date(1993, 1, 1)
        )

        # should not be able to specify the month and quarter
        self.assertRaises(ValueError, date_engine.timestamp2date, 1992, 5, 1)

    def test_isodate2timestamp(self):
        self.assertEqual(
            date_engine.isodate2timestamp(101, '2014-05-03'),
            '042014'
        )

        self.assertEqual(
            date_engine.isodate2timestamp('101', '2014-01-05'),
            '122013'
        )

    def test_year_start_isodate(self):
        self.assertEqual(
            date_engine.year_start_isodate(1988),
            '1988-01-01'
        )

        self.assertEqual(
            date_engine.year_start_isodate(2015),
            '2015-01-01'
        )

    def test_is_isodate(self):
        self.assertTrue(date_engine.is_isodate('2015-04-30'))
        self.assertTrue(date_engine.is_isodate('2011-01-01'))
        self.assertTrue(date_engine.is_isodate('1988-12-31'))
        self.assertFalse(date_engine.is_isodate('1988-12-32'))
        self.assertFalse(date_engine.is_isodate('25-12-1995'))
        self.assertFalse(date_engine.is_isodate('12-25-1995'))

if __name__ == '__main__':
    unittest.main()
