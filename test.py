import unittest, os, uuid, shutil, datetime, time
from filecrypt.filecrypt import FileCrypt
from pprint import pprint

class MyTest(unittest.TestCase):
	__rootdir = os.path.abspath(os.sep)
	__unencrypted_content = "foo bar baz"
	__password = str(uuid.uuid4())[:8]

	def setUp(self):
		self.__tmpdir = os.path.join(self.__rootdir, 'tmp', 'filecrypt-test-'+self.__get_datetime_string())
		os.mkdir(self.__tmpdir)
		self.__unencrypted_filename = os.path.join(self.__tmpdir, 'test.txt');
		self.__encrypted_filename = os.path.join(self.__tmpdir, 'test.txt.fc');		
		self.filecrypt = FileCrypt()

	def tearDown(self):
		shutil.rmtree(self.__tmpdir)
		# pass

	### tests

	def testBasicEncryptingAndDecrypting(self):
		self.__create_test_file()
		self.__encryptfile()
		os.remove(self.__unencrypted_filename)
		self.__decryptfile()
		with open(self.__unencrypted_filename, 'r') as text_file:
			content = text_file.read()
		self.assertEqual(self.__unencrypted_content, content)

	#### helpers	

	def __create_test_file(self, filename=None, content=None):
		filename = self.__unencrypted_filename if filename == None else filename
		content = self.__unencrypted_content if content == None else content
		with open(filename, "w") as text_file:
			text_file.write(content)

	def __encryptfile(self, in_filename=None, out_filename=None, password=None):
		in_filename = self.__unencrypted_filename if in_filename == None else in_filename
		out_filename = self.__encrypted_filename if out_filename == None else out_filename
		password = self.__password if password == None else out_filename
		self.filecrypt.encryptfile(in_filename, out_filename, password)

	def __decryptfile(self, in_filename=None, out_filename=None, password=None):
		in_filename = self.__encrypted_filename if in_filename == None else in_filename
		out_filename = self.__unencrypted_filename if out_filename == None else out_filename
		password = self.__password if password == None else out_filename
		self.filecrypt.decryptfile(in_filename, out_filename, password)		

	def __get_datetime_string(self):
		ts = time.time()
		return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')

if __name__ == '__main__':
    unittest.main()		