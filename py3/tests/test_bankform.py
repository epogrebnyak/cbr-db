import sys
sys.path.append('..')

import unittest
import bankform
import collections

class BankformTest(unittest.TestCase):

    def test_get_db_name_single(self):
        for key in ('raw', 'final'):
            arg = {'raw': True, 'final': False}
            names = bankform.get_db_name(arg)
            self.assertIsInstance(names, collections.Iterable)
            self.assertIsInstance(names[0], str)
            self.assertTrue(len(names) == 1)

    def test_get_db_name_all(self):
            arg = {'raw': False, 'final': False}
            names = bankform.get_db_name(arg)
            self.assertIsInstance(names, collections.Iterable)
            self.assertIsInstance(names[0], str)
            self.assertTrue(len(names) == 2)

if __name__ == '__main__':
    unittest.main()
