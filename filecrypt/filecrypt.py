# sudo pip install pycrypto

## from http://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible
## looking into password protecting files
import getpass, os, re, shutil, uuid

from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
from pprint import pprint

class InvalidPasswordError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class InvalidFileTypeError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class InvalidFileContentError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class SameInputOutputFileError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class InvalidFileError(IOError):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class FileCrypt:
    bs = AES.block_size
    prefix = 'filecrypt__'
    mode = AES.MODE_CBC
    extension = 'fc'

    ## TODO: add some logic in here about the .fc extension, but raise errors rather than outputting to screen as in __main__
    def encryptfile(self, in_filename, password, out_filename=None, key_length=32):
        if out_filename == None:
            out_filename = self.add_extension(in_filename)
        if in_filename == out_filename:
            raise SameInputOutputFileError('Input and output files cannot be same')

        try:
            with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
                self.encrypt(in_file, out_file, password)
        except IOError as ioe:
            raise InvalidFileError(ioe.strerror + ': ' + ioe.filename)


    def decryptfile(self, in_filename, password, out_filename=None, key_length=32):
        if out_filename == None:
            out_filename = self.remove_extension(in_filename)
        if in_filename == out_filename:
            raise SameInputOutputFileError('Input and output files cannot be same')
        try:
            with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
                ## check for valid prefix
                content = in_file.read()
                prefix = content[:len(self.prefix)]
                if prefix != self.prefix:
                    raise InvalidFileTypeError('Invalid file type. Not a filecrypt file.')
                in_file.seek(0)
                ## decrypt file
                try:
                    self.decrypt(in_file, out_file, password)
                except ValueError as ve:
                    raise InvalidFileContentError('Something went wrong. Perhaps the encrypted file is corrupted. The message is: '+ve.message)
        except IOError as ioe:
            raise InvalidFileError(ioe.strerror + ': ' + ioe.filename)

        ## check contents
        with open(out_filename, 'rb') as out_file:
            content = out_file.read()
        if content == '':
            raise  InvalidPasswordError('Invalid password')

    def add_extension(self, filename):
        return filename + '.' + self.extension

    def remove_extension(self, filename):
        return re.sub(r'\.'+self.extension+'$', "", filename)


    def encrypt(self, in_file, out_file, password, key_length=32):
        salt = Random.new().read(self.bs - len(self.prefix))
        key, iv = self.__derive_key_and_iv(password, salt, key_length, self.bs)
        cipher = self.__get_cypher(key, iv)
        out_file.write(self.prefix + salt)
        finished = False
        while not finished:
            chunk = in_file.read(1024 * self.bs)
            if len(chunk) == 0 or len(chunk) % self.bs != 0:
                padding_length = (self.bs - len(chunk) % self.bs) or self.bs
                chunk += padding_length * chr(padding_length)
                finished = True
            out_file.write(cipher.encrypt(chunk))

    def decrypt(self, in_file, out_file, password, key_length=32):
        salt = in_file.read(self.bs)[len(self.prefix):]
        key, iv = self.__derive_key_and_iv(password, salt, key_length, self.bs)
        cipher = self.__get_cypher(key, iv)
        next_chunk = ''
        finished = False
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * self.bs))
            if len(next_chunk) == 0:
                padding_length = ord(chunk[-1])
                chunk = chunk[:-padding_length]
                finished = True
            out_file.write(chunk)

    def get_new_password(self):
        pswd = None
        while True:
            pswd = getpass.getpass('Password: ')
            pswd2 = getpass.getpass('Repeat password: ')
            if pswd2 == pswd:
                break
            print('* Passwords do not match')
        return pswd

    def get_password(self):
        return getpass.getpass('Password: ')


    def __derive_key_and_iv(self, password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]

    def __get_cypher(self, key, iv):
        return AES.new(key, self.mode, iv)
