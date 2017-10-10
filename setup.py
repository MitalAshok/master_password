#!/usr/bin/env python

from setuptools import setup, find_packages

import sys
import unittest

from codecs import open
from os import path


__dir__ = path.abspath(path.dirname(__file__))

# To prevent a redundant __version__, import it from the packages
sys.path.insert(0, __dir__)

try:
    from master_password import (
        __version__, __author__, __author_email__, __license__
    )
finally:
    sys.path.pop(0)

with open(path.join(__dir__, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def test_suite():
    test_loader = unittest.TestLoader()
    return test_loader.discover(__dir__, pattern='tests*.py')

setup_args = dict(
    name='master_password',

    version=__version__,

    description='An implementation of the Master Password\xa9 algorithm in Python',
    long_description=long_description,

    url='https://github.com/MitalAshok/master_password',

    author=__author__,
    author_email=__author_email__,

    license=__license__,

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Topic :: Security',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords=['masterpassword', 'statelesspassword', 'password'],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Avoid downloading extra dependencies if hashlib.scrypt may be available
    install_requires=[],

    # $ pip install master_password[scrypt]
    # $ pip install master_password[pyscrypt]
    # $ pip install master_password[crypto]
    extras_require={
        'scrypt': ['scrypt'],
        'pyscrypt': ['pyscrypt'],
        'crypto': ['cryptography']
    },


    entry_points={
        'console_scripts': [
            'master_password=master_password.__main__:main',
        ]
    },

    test_suite='setup.test_suite'
)


setup(**setup_args)
