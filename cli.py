import argparse, os, re, shutil, sys
from pprint import pprint

from filecrypt import (FileCrypt, InvalidPasswordError, InvalidFileTypeError, InvalidFileContentError, 
    SameInputOutputFileError, InvalidFileError
)

class Cli:
    @staticmethod
    def main():
        ## arguments
        parser = argparse.ArgumentParser(prog='filecrypt', description='Encrypt and decrypt files with password protection')
        parser.add_argument('action', help='Action to take', choices=set(('encrypt', 'decrypt')))
        parser.add_argument('file', help='File to encrypt or decrypt. By default will add ".fc" extension when encryting and remove when decrypting')
        parser.add_argument('-d', '--delete-original', action="store_true", help='Delete original file')
        parser.add_argument('-o', '--output-file', help='Custom output file')
        args = parser.parse_args()
        ## let's do this
        filecrypt = FileCrypt()
        ## encrypting
        if args.action == 'encrypt':
            password = filecrypt.get_new_password() 
            try:      
                filecrypt.encryptfile(args.file, password, args.output_file, args.delete_original)
                output_file = filecrypt.add_extension(args.file) if args.output_file == None else args.output_file
                print('* '+args.file+' encrypted as ' + output_file)
            except (SameInputOutputFileError, InvalidFileError) as e:
                print('* ' + e.message)
                exit(1)
        ## decrypting
        elif args.action == 'decrypt':
            password = filecrypt.get_password()
            try:
                filecrypt.decryptfile(args.file, password, args.output_file, args.delete_original)
                output_file = filecrypt.remove_extension(args.file) if args.output_file == None else args.output_file
                print('* '+args.file+' decrypted as ' + output_file)
            except (InvalidPasswordError, InvalidFileTypeError, InvalidFileError, InvalidFileContentError, SameInputOutputFileError) as e: 
                print('* ' + e.message)
                exit(1)

        if args.delete_original:
            print('* '+args.file+' deleted')