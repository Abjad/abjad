#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools
import sys

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

long_description = 'Abjad is an interactive software system designed'
long_description += ' to help composers build up complex pieces of'
long_description += ' music notation in an iterative and incremental way.'
long_description += ' Use Abjad to create a symbolic representation of all'
long_description += ' the notes, rests, staves, tuplets, beams and slurs'
long_description += ' in any score.'
long_description += ' Because Abjad extends the Python programming language,'
long_description += ' you can use Abjad to make systematic changes to'
long_description += ' your music as you work.'
long_description += ' And because Abjad wraps the powerful LilyPond music'
long_description += ' notation package, you can use Abjad to control'
long_description += ' the typographic details of all the symbols on the page.'

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
    'Sphinx >= 1.0.7',
    'configobj >= 4.7.2',
    'ply >= 3.4',
    'pytest >= 2.1',
    ]
if sys.version_info[0] == 2:
    install_requires.append('enum34')

setuptools.setup(
    author=author,
    author_email=author_email,
    description=description,
    entry_points={
        'console_scripts': [
            'abjad = abjad.tools.systemtools.run_abjad:run_abjad',
            'ajv = abjad.tools.developerscripttools.run_ajv:run_ajv',
            ]
        },
    include_package_data=True,
    install_requires=install_requires,
    keywords=keywords,
    license='GPL',
    long_description=long_description,
    name='Abjad',
    packages=(
        'abjad',
        ),
    platforms='Any',
    url='http://www.projectabjad.org',
    version=__version__,
    )