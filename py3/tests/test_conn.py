#  should be run from the parent directory, as:
#  set PYTHONPATH=%PYTHONPATH;.
#  python tests/test_conn.py
import unittest
import collections
import conn

class ConnectionTest(unittest.TestCase):
    def test_select(self):
        resp = conn.execute_sql('SELECT 5')
        self.assertEqual(len(resp), 1)
        self.assertEqual(len(resp[0]), 1)
        self.assertEqual(resp[0][0], 5)
        
    def test_return(self):
        # should return at least 1 result
        resp = conn.execute_sql('SHOW DATABASES');
        self.assertTrue(isinstance(resp, collections.Iterable))
        self.assertTrue(len(resp) > 0)
                
        # empty set
        resp = conn.execute_sql('SHOW DATABASES WHERE "Database" = "xASFghd9"');
        self.assertTrue(isinstance(resp, collections.Iterable))
        self.assertEqual(len(resp), 0)

if __name__ == '__main__':
    unittest.main()