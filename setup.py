#!/usr/bin/env python

from setuptools import setup
import subprocess

__version__ = subprocess.check_output('git describe --always --dirty'.split(' ')).decode().splitlines()[0]
print('VERSION: ' + __version__)

setup(
    version = __version__,

    entry_points={
        'console_scripts': [
            'bsdl2json = bsdl_parser.bsdl2json:main',
        ],
    },
    
    packages = ['bsdl_parser'],
    install_requires = ['grako']
)
