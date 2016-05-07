import argparse, os, re, shutil, sys
from pprint import pprint

from filecrypt.filecrypt import FileCrypt, BadPasswordException

def main():
    ## arguments
    parser = argparse.ArgumentParser(prog='filecrypt', description='Encrypt and decrypt files with password protection')
    parser.add_argument('action', help='Action to take', choices=set(('encrypt', 'decrypt')))
    parser.add_argument('file', help='File to encrypt or decrypt. By default will add ".fc" extension when encryting and remove when decrypting')
    parser.add_argument('-d', '--delete-original', action="store_true", help='Delete original file')
    parser.add_argument('-o', '--output-file', help='Custom output file')
    args = parser.parse_args()
    # pprint(args)
    ## let's do this
    filecrypt = FileCrypt()
    ## encrypting
    if args.action == 'encrypt':
        password = filecrypt.get_new_password()
        if args.output_file == None:
            args.output_file = args.file + '.fc'        
        filecrypt.encryptfile(args.file, args.output_file, password)
        print('* '+args.file+' encrypted as '+args.output_file)
    ## decrypting
    elif args.action == 'decrypt':
        password = filecrypt.get_password()
        if args.output_file == None:
            args.output_file = num = re.sub(r'\.fc$', "", args.file) 
            ## input and output files are the same
            if args.output_file == args.file:
                answer = raw_input('Output and input files are same. Overwrite input file? [y/N]')
                ## exit
                if answer.lower() != 'y':
                    print('* Add a .fc extension to input file or specify an output file with -o or --output-file')
                    exit()
                ## copy source file to tmp dir
                else:
                    rootdir = os.path.abspath(os.sep)
                    import uuid
                    filename = str(uuid.uuid4())
                    print(filename, rootdir)
                    tmpfile = os.path.join(rootdir, 'tmp', filename)
                    shutil.copyfile(args.file, tmpfile)
                    os.remove(args.file)
                    args.file = tmpfile
        try:
            filecrypt.decryptfile(args.file, args.output_file, password)
            print('* '+args.file+' decrypted as '+args.output_file)
        except: 
            print('* Invalid password')

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