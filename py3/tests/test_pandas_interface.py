'''
Created on Jun 25, 2015

@author: bhanu
'''
import unittest
import pandas_interface as pdi
import pandas as pd
from pandas.util.testing import assert_frame_equal


class Test(unittest.TestCase):


    def test_make_balance(self):
        con = pdi.get_sqla_connection()
        self.assertNotEqual(None, con, msg="connection to sql database failed")
        balance_df = pdi.make_balance()
        balance_table = pd.read_sql_table('balance', con)
        assert_frame_equal(balance_df, balance_table, 
                           check_names=True, 
                           check_dtype=True)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_make_balance']
    unittest.main()