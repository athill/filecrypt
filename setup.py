import ez_setup
ez_setup.use_setuptools()

import os
from setuptools import setup, find_packages
# setup(
#     name = "filecrypt",
#     version = "0.1",
#     packages = find_packages(),
# )


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "filecrypt",
    version = "0.0.4",
    author = "Andy Hill",
    author_email = "andy@andyhill.us",
    description = ("An demonstration of how to create, document, and publish "
                                   "to the cheese shop a5 pypi.org."),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/filecrypt",
    packages=['filecrypt'],
    long_description=read('readme.md'),
    install_requires = ['pycrypto'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)