import ez_setup
ez_setup.use_setuptools()

import os
from setuptools import setup # s, find_packages
# setup(
#     name = "filecrypt",
#     version = "0.1",
#     packages = find_packages(),
# )

url = "https://github.com/athill/filecrypt"
requires = ['pycrypto']

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "athill-filecrypt",
    version = "0.0.4",
    author = "Andy Hill",
    author_email = "andy@andyhill.us",
    description = ("Password protect files."),
    entry_points = {
        "console_scripts": ['filecrypt = cli.Cli:main']
    },    
    license = "BSD",
    keywords = "encode decode encrypt file",
    url = url,
    download_url = 'https://github.com/athill/filecrypt/archive/master.zip',
    long_description=read('readme.md'),

    install_requires = requires,
    requires = requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)