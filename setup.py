#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import os
version_file_path = os.path.join(
    os.path.dirname(__file__),
    'abjad',
    '_version.py'
    )
execfile(version_file_path, {}, locals())

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
    install_requires=[
        'pytest >= 2.1',
        'Sphinx >= 1.0.7',
        'ply >= 3.4',
        'configobj >= 4.7.2',
        ],
    keywords=keywords,
    license='GPL',
    long_description=long_description,
    name='Abjad',
    packages=setuptools.find_packages(exclude='experimental'),
    platforms='Any',
    url='http://www.projectabjad.org',
    version=__version__,
    )
