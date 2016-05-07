import unittest, os, uuid, shutil, datetime, time
from filecrypt.filecrypt import FileCrypt, InvalidPasswordError, InvalidFileTypeError, InvalidFileContentError, SameInputOutputFileError, InvalidFileError
from pprint import pprint

counter = 0

class FilecryptTest(unittest.TestCase):
	__rootdir = os.path.abspath(os.sep)
	__unencrypted_content = "foo bar baz"
	__password = str(uuid.uuid4())[:8]
	__dir_index = 0

	def setUp(self):
		global counter
		self.__tmpdir = os.path.join(self.__rootdir, 'tmp', 'filecrypt-test-'+self.__get_datetime_string()+'-'+str(counter))
		counter = counter + 1
		os.mkdir(self.__tmpdir)
		self.__unencrypted_filename = os.path.join(self.__tmpdir, 'test.txt');
		self.__encrypted_filename = os.path.join(self.__tmpdir, 'test.txt.fc');		
		self.filecrypt = FileCrypt()

	def tearDown(self):
		shutil.rmtree(self.__tmpdir)
		pass

	### tests

	def testBasicEncryptingAndDecrypting(self):
		self.__create_test_file()
		self.__encryptfile()
		self.__remove_test_file()
		self.__decryptfile()
		content = self.__read_test_file()
		self.assertEqual(self.__unencrypted_content, content)

	def testDecryptFailsIfBadPassword(self):
		self.__create_test_file()
		self.__encryptfile()
		self.__remove_test_file()
		with self.assertRaises(InvalidPasswordError) as context:
			self.__decryptfile(password='foobar')
		self.assertTrue('Invalid password' in context.exception)

	def testDecryptFailsIfBadFileType(self):
		with open(self.__encrypted_filename, 'wb') as encryted_file:
			encryted_file.write('foo bar baz')
		with self.assertRaises(InvalidFileTypeError) as context:
			self.__decryptfile()
		self.assertTrue('Invalid file type. Not a filecrypt file.' in context.exception)

	def testDecryptFailsIfBadContentType(self):
		with open(self.__encrypted_filename, 'wb') as encryted_file:
			encryted_file.write(self.filecrypt.prefix+'foo bar baz')
		with self.assertRaises(InvalidFileContentError) as context:
			self.__decryptfile()
		self.assertTrue('Something went wrong. Perhaps the encrypted file is corrupted.' in context.exception.message)

	def testDecryptFailsIfSameFileName(self):
		with self.assertRaises(SameInputOutputFileError) as context:
			self.__decryptfile(in_filename=self.__unencrypted_filename)
		self.assertTrue('Input and output files cannot be same' in context.exception)

	def testEncryptFailsIfSameFileName(self):
		with self.assertRaises(SameInputOutputFileError) as context:
			self.__encryptfile(out_filename=self.__unencrypted_filename)
		self.assertTrue('Input and output files cannot be same' in context.exception)

	def testDecryptFailsIfSameInfileDoesntExist(self):
		with self.assertRaises(InvalidFileError) as context:
			self.__decryptfile(in_filename='foo')
		self.assertTrue(context.exception.message in context.exception)

	def testEncryptFailsIfSameInfileDoesntExist(self):
		with self.assertRaises(InvalidFileError) as context:
			self.__encryptfile(in_filename='foo')
		self.assertTrue(context.exception.message in context.exception)

	def testDecryptRemovesExtensionByDefault(self):
		self.__create_test_file()
		self.filecrypt.encryptfile(self.__unencrypted_filename, self.__password, self.__encrypted_filename)
		self.__remove_test_file()
		self.filecrypt.decryptfile(self.__encrypted_filename, self.__password)
		self.assertTrue(os.path.exists(self.__unencrypted_filename))

	def testEncryptAddsExtensionByDefault(self):		
		self.__create_test_file()
		self.filecrypt.encryptfile(self.__unencrypted_filename, self.__password)
		self.assertTrue(os.path.exists(self.__encrypted_filename))

	def testAddExtension(self):
		filename = 'foo'
		expected = filename+'.'+self.filecrypt.extension
		actual = self.filecrypt.add_extension(filename)
		self.assertEqual(expected, actual)

	def testRemoveExtension(self):
		filename = 'foo'
		expected = filename
		actual = self.filecrypt.remove_extension(filename+'.'+self.filecrypt.extension)
		self.assertEqual(expected, actual)

	#### helpers	

	def __create_test_file(self, filename=None, content=None):
		filename = self.__unencrypted_filename if filename == None else filename
		content = self.__unencrypted_content if content == None else content
		with open(filename, "w") as text_file:
			text_file.write(content)

	def __remove_test_file(self, filename=None):
		filename = self.__unencrypted_filename if filename == None else filename
		os.remove(filename)

	def __read_test_file(self, filename=None):
		filename = self.__unencrypted_filename if filename == None else filename
		with open(filename, 'r') as text_file:
			content = text_file.read()
		return content

	def __encryptfile(self, in_filename=None, password=None, out_filename=None,):
		in_filename = self.__unencrypted_filename if in_filename == None else in_filename
		out_filename = self.__encrypted_filename if out_filename == None else out_filename
		password = self.__password if password == None else out_filename
		self.filecrypt.encryptfile(in_filename, password, out_filename)

	def __decryptfile(self, in_filename=None, password=None, out_filename=None):
		in_filename = self.__encrypted_filename if in_filename == None else in_filename
		out_filename = self.__unencrypted_filename if out_filename == None else out_filename
		password = self.__password if password == None else out_filename

		self.filecrypt.decryptfile(in_filename, password, out_filename)

	def __get_datetime_string(self):
		ts = time.time()
		return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')

if __name__ == '__main__':
    unittest.main()		