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

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Artistic Software',
    ]

install_requires = [
    'ply',
    'six',
    ]
version = '.'.join(str(x) for x in sys.version_info[:3])
if StrictVersion(version) < StrictVersion('3.4.0'):
    install_requires.append('enum34')
    install_requires.append('pathlib2')
if StrictVersion(version) < StrictVersion('3.3.0'):
    install_requires.append('funcsigs')
    install_requires.append('mock')

extras_require = {
    'development': [
        'pytest>=3.0.0',
        'sphinx>=1.4',
        'sphinx-rtd-theme',
        'PyPDF2',
        ],
    'ipython': [
        'ipython',
        'jupyter',
        ],
    }

entry_points = {
    'console_scripts': [
        'abjad = abjad.tools.systemtools.run_abjad:run_abjad',
        'ajv = abjad.tools.commandlinetools.run_ajv:run_ajv',
        ]
    }

if __name__ == '__main__':
    setuptools.setup(
        author=author,
        author_email=author_email,
        classifiers=classifiers,
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
