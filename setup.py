#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools
import sys
from distutils.version import StrictVersion

version_file_path = os.path.join(
    os.path.dirname(__file__),
    'abjad',
    '_version.py'
    )
with open(version_file_path, 'r') as file_pointer:
    file_contents_string = file_pointer.read()
local_dict = {}
exec(file_contents_string, None, local_dict)
__version__ = local_dict['__version__']

description = 'Abjad is a Python API for Formalized Score Control.'

with open('README.rst', 'r') as file_pointer:
    long_description = file_pointer.read()

author = [
    'Trevor Bača',
    'Josiah Wolf Oberholtzer',
    'Víctor Adán',
    ]
author = ', '.join(author)

author_email = [
    'trevorbaca@gmail.com',
    'josiah.oberholtzer@gmail.com',
    'contact@victoradan.net',
    ]
author_email = ', '.join(author_email)

keywords = [
    'music composition',
    'music notation',
    'formalized score control',
    'lilypond',
    ]
keywords = ', '.join(keywords)

install_requires = [
    'ply',
    'six',
    ]
version = '.'.join(str(x) for x in sys.version_info[:3])
if StrictVersion(version) < StrictVersion('3.4.0'):
    install_requires.append('enum34')

extras_require = {
    'development': [
        'pytest',
        'sphinx>=1.3.1',
        'PyPDF2',
        ],
    'ipython': [
        'ipython',
        ],
    }

entry_points = {
    'console_scripts': [
        'abjad = abjad.tools.systemtools.run_abjad:run_abjad',
        'ajv = abjad.tools.developerscripttools.run_ajv:run_ajv',
        ]
    }

if __name__ == '__main__':
    setuptools.setup(
        author=author,
        author_email=author_email,
        description=description,
        entry_points=entry_points,
        extras_require=extras_require,
        include_package_data=True,
        install_requires=install_requires,
        keywords=keywords,
        license='GPL',
        long_description=long_description,
        name='Abjad',
        packages=['abjad'],
        platforms='Any',
        url='http://www.projectabjad.org',
        version=__version__,
        )