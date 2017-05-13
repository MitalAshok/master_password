from setuptools import setup, find_packages

from codecs import open
from os import path

__version__ = '1.0.0'

__dir__ = path.abspath(path.dirname(__file__))


with open(path.join(__dir__, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup_args = dict(
    name='master_password',

    version=__version__,

    description='An implementation of the Master Password\xa9 algorithm in Python',
    long_description=long_description,

    url='https://github.com/MitalAshok/master_password',

    author='MitalAshok',
    author_email='mital.vaja[AT]googlemail.com',

    license='GPL-3.0',

    classifiers=[
        'Development Status :: 3 - Alpha',

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
    extras_require={
        'scrypt': ['scrypt'],
        'pyscrypt': ['pyscrypt']
    },


    entry_points={
        'console_scripts': [
            'master_password=master_password.__main__:main',
        ]
    }
)


setup(**setup_args)
