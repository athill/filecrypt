# sudo pip install pycrypto

## from http://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible
## looking into password protecting files
import argparse, getpass, os, re, shutil, sys

from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
from pprint import pprint

class FileCrypt:
    bs = AES.block_size
    prefix = 'Salted__'
    mode = AES.MODE_CBC


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
        self.bs = AES.block_size
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
        print(out_file.read())

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