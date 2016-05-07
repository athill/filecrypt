# filecrypt

Python 2 script to encypt/decrypt files with password. Basically a CLI/API around [this stackoverflow answer](http://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible)

## requires

	pycrypt

via `pip` or `easy_install`

## usage

### Basic usage:

	$ echo 'foo bar baz' > test.txt
	$ /path/to/filecrypt encrypt test.txt
	# enter password and confirm
	$ rm test.txt
	$ /path/to/filecrypt decrypt test.txt.fc
	# enter password
	$ less test.txt
	foo bar baz

### Documentation
	
	positional arguments:
	  {decrypt,encrypt}     Action to take
	  file                  File to encrypt or decrypt. By default will add ".fc"
	                        extension when encryting and remove when decrypting

	optional arguments:
	  -h, --help            show this help message and exit
	  -d, --delete-original
	                        Delete original file
	  -o OUTPUT_FILE, --output-file OUTPUT_FILE
	                        Custom output file