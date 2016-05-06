import unittest, os, uuid, shutil
from filecrypt.filecrypt import FileCrypt
from pprint import pprint

class MyTest(unittest.TestCase):
	__rootdir = os.path.abspath(os.sep)


	def setUp(self):
		self.__tmpdir = os.path.join(self.__rootdir, 'tmp', 'filecrypt-test-'+str(uuid.uuid4())[:8])
		os.mkdir(self.__tmpdir)

	def tearDown(self):
		shutil.rmtree(self.__tmpdir)

	def test(self):
		self.assertEqual(4, 4)


if __name__ == '__main__':
    unittest.main()		