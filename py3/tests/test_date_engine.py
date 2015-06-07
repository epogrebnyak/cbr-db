import unittest
from datetime import datetime
import date_engine

class DateEngineTest(unittest.TestCase):
    def test_shift_month_ahead(self):
        self.assertEqual(
            date_engine.shift_month_ahead(datetime(2015, 5, 2)),
            datetime(2015, 6, 2)
        )

        self.assertEqual(
            date_engine.shift_month_ahead(datetime(2012, 12, 23)),
            datetime(2013, 1, 23)
        )
        
        # what should occur in this case?
        self.assertEqual(
            date_engine.shift_month_ahead(datetime(2013, 3, 31)),
            datetime(2013, 4, 30)
        )
    
    def test_get_date_range(self):
        pass
    
    def test_get_isodate_list(self):
        pass
    
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
            date_engine.datetime2iso(datetime(1988, 1, 1)),        
            '1988-01-01'
        )
        
        self.assertEqual(
            date_engine.datetime2iso(datetime(2015, 5, 23)),        
            '2015-05-23'
        )
    
    def test_iso2datetime(self):
        self.assertEqual(
            date_engine.iso2datetime('1988-01-01'),        
            datetime(1988, 1, 1)
        )
        
        self.assertEqual(
            date_engine.iso2datetime('2015-05-23'),        
            datetime(2015, 5, 23)
        )
    
    def test_isodate2timestamp(self):
        pass
    
    def test_date2timestamp(self):
        pass
    
    def test_timestamp2date(self):
        pass
    
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