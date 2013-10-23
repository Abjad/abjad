#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import setuptools
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    import setuptools

import os
version_file_path = os.path.join(
    os.path.dirname(__file__), 
    'abjad', 
    '_version.py'
    )
execfile(version_file_path, {}, locals())

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
    name='Abjad',
    version=__version__,
    description='Abjad is a Python API for Formalized Score Control.',
    long_description=long_description,
    author='Trevor Baca, Josiah Wolf Oberholtzer, Victor Adan',
    author_email=author_email,
    url='http://www.projectabjad.org',
    keywords=keywords,
    license='GPL',
    platforms='Any',
    install_requires=[
        'pytest >= 2.1',
        'Sphinx >= 1.0.7',
        'ply >= 3.4',
        'configobj >= 4.7.2',
        ],
    # include all packages found in '.'
    packages=setuptools.find_packages(),
    #scripts = ['ez_setup.py'],
    # include all file types under abjad
    include_package_data=True,
    entry_points={'console_scripts':[
        'abjad = abjad.tools.iotools.run_abjad:run_abjad',
        'abjad-book = abjad.tools.abjadbooktools.run_abjad_book:run_abjad_book',
        'abj-dev = abjad.tools.developerscripttools.run_abjdev:run_abjdev',
        'ajv = abjad.tools.developerscripttools.run_abjdev:run_abjdev',
        ]},
    )
