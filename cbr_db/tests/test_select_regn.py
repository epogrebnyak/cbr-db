import sys
sys.path.append('..')

import unittest
from cbr_db import bankform
from cbr_db import conn

def get_regns():
    return sorted([
        t[0] for t in 
        conn.execute_sql("SELECT regn FROM cfg_regn_in_focus",
                         database="dbf_db3")
    ])

class SelectRegn(unittest.TestCase):
    def test_regn_list_one(self):
        bankform.main("make dataset 101 2015 --regn=964".split(' '))
        self.assertEqual(
            get_regns(),
            [964]
        )
    
    def test_regn_list_many(self):
        bankform.main("make dataset 101 2015 --regn=2,5,3,1".split(' '))
        self.assertEqual(
            get_regns(),
            [1, 2, 3, 5]
        )
    
    def test_regn_all(self):
        """warning: this tests depends on the current database contents, that
        must be populated."""
        bankform.main("make dataset 101 2015".split(' '))
        regns1 = get_regns()
        
        bankform.main("make dataset 101 2015 --regn-all".split(' '))
        regns2 = get_regns()
        
        self.assertEqual(regns1, regns2)
    
    def test_regn_list_file(self):
        bankform.main("make dataset 101 2015 --regn-file=regn.txt".split(' '))
        self.assertEqual(
            get_regns(),
            [10, 11, 12, 13, 14, 15]
        )
    
if __name__ == '__main__':
    unittest.main()