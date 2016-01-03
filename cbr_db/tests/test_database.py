import sys
sys.path.append('..')

import unittest
import database

class DatabaseTest(unittest.TestCase):
    def test_sqldump_table_and_filename(self):
        self.assertEqual(
            database.get_sqldump_table_and_filename('101'),
            ('f101', 'f101.sql')
        )
        
        self.assertEqual(
            database.get_sqldump_table_and_filename('102'),
            ('f102', 'f102.sql')
        )
    
if __name__ == '__main__':
    unittest.main()