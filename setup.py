#!/usr/bin/env python
"""
To install the Python REST API for Pure Storage:
Change to the directory you have cloned this git repo and run:
"sudo pip install ."
"""
import pkg_resources
from setuptools import setup

__version__ = '1.2-drives'
packages = [ 'purestorage_rest_api' ]
commands = ['rest_api = purestorage_rest_api.rest_session:main']

setup(
    name                = 'PureStorage_RestAPI',
    version             = __version__,
    description         = 'Pure Storage REST API Tool For FlashArray',
    author              = 'Mitch O\'Donnell',
    author_email        = 'devreap1@gmail.com',
    packages            = packages,
    url                 = 'https://github.com/BuildAndDestroy/PureStorage_RestAPI',
    license             = open('LICENSE').read(),
    install_requires    = ['argparse', 'purestorage', 'prettytable'],
    entry_points        = {'console_scripts': commands},
    prefix              = '/opt/PureStorage_RestAPI',
    long_description    = open('README.md').read()
)
