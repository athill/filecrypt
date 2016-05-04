import unittest, os
from . import FileCrypt
from pprint import pprint

class MyTest(unittest.TestCase):
	def test(self):
		pprint(dir(__main__))
		self.assertEqual(4, 4)


if __name__ == '__main__':
    unittest.main()		