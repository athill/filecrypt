# sudo pip install pycrypto

## from http://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible
## looking into password protecting files
import argparse, getpass, os, re, shutil, sys

# from hashlib import md5
# from Crypto.Cipher import AES
# from Crypto import Random
from pprint import pprint


from filecrypt.filecrypt import FileCrypt

## usage

def main():
    parser = argparse.ArgumentParser(prog='filecrypt', description='Encrypt and decrypt files with password protection')
    parser.add_argument('action', help='Action to take', choices=set(('encrypt', 'decrypt')))
    parser.add_argument('file', help='File to encrypt or decrypt. By default will add ".fc" extension when encryting and remove when decrypting')
    parser.add_argument('-d', '--delete-original', action="store_true", help='Delete original file')
    parser.add_argument('-o', '--output-file', help='Custom output file')
    args = parser.parse_args()
    pprint(args)
    filecrypt = FileCrypt()
    if args.action == 'encrypt':
        pswd = filecrypt.get_new_password()
        if args.output_file == None:
            args.output_file = args.file + '.fc'
        with open(args.file, 'rb') as in_file, open(args.output_file, 'wb') as out_file:
            filecrypt.encrypt(in_file, out_file, pswd)            
        print('* '+args.file+' encrypted as '+args.output_file)
    elif args.action == 'decrypt':
        pswd = filecrypt.get_password()
        if args.output_file == None:
            args.output_file = num = re.sub(r'\.fc$', "", args.file) 
            if args.output_file == args.file:
                answer = raw_input('Output and input files are same. Overwrite input file? [y/N]')
                if answer.lower() != 'y':
                    print('* Add a .fc extension to input file or specify an output file with -o or --output-file')
                    exit()
                else:
                    # files have same name, copy source file to tmp dir
                    rootdir = os.path.abspath(os.sep)
                    import uuid
                    filename = str(uuid.uuid4())
                    print(filename, rootdir)
                    tmpfile = os.path.join(rootdir, 'tmp', filename)
                    shutil.copyfile(args.file, tmpfile)
                    os.remove(args.file)
                    args.file = tmpfile
        with open(args.file, 'rb') as in_file, open(args.output_file, 'a+b') as out_file:
            filecrypt.decrypt(in_file, out_file, pswd)
            print('* '+args.file+' decrypted as '+args.output_file)

    if args.delete_original:
        os.remove(args.file)
        print('* '+args.file+' deleted')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nProcess interrupted by user')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) 