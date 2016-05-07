# filecrypt

Python 2 script to encypt/decrypt files with password. Basically a UI/API around [this stackoverflow answer](http://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible)

## requires

	pycrypt

via `pip` or `easy_install`

## usage

	Encrypt and decrypt files with password protection

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