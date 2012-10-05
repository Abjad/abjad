#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ez_setup import use_setuptools

# following line must come before import setup
use_setuptools()
from setuptools import find_packages
from setuptools import setup


setup(name = 'Abjad', 
    version = '2.10',
    description = 'Abjad is a Python API for Formalized Score Control.',
    long_description = 'Abjad is an interactive software system designed to help composers build up complex pieces of music notation in an iterative and incremental way. Use Abjad to create a symbolic representation of all the notes, rests, staves, tuplets, beams and slurs in any score. Because Abjad extends the Python programming language, you can use Abjad to make systematic changes to your music as you work. And because Abjad wraps the powerful LilyPond music notation package, you can use Abjad to control the typographic details of all the symbols on the page.',
    author = 'Trevor Baca, Josiah Oberholtzer, Victor Adan',
    author_email = 'trevorbaca@gmail.com, josiah.oberholtzer@gmail.com, contact@victoradan.net',
    url = 'http://www.projectabjad.org',
    keywords = 'music composition, music notation, formalized score control, lilypond',
    license = 'GPL',
    platforms = 'Any',
    install_requires = [
        'pytest >= 2.1',
        'Sphinx >= 1.0.7',
        'ply >= 3.4',
        'configobj >= 4.7.2',
        ],
    # include all packages found in '.'
    packages = find_packages(),
    #scripts = ['ez_setup.py'],
    # include all file types under abjad
    include_package_data = True,
    entry_points = {'console_scripts':[
        'abj = abjad.tools.iotools._run_abjad:_run_abjad',
        'abjad = abjad.tools.iotools._run_abjad:_run_abjad',
        'abjad-book = abjad.tools.abjadbooktools._run_abjad_book:_run_abjad_book',
        'abj-dev = abjad.tools.developerscripttools._run_abjdev:_run_abjdev',
        'ajv = abjad.tools.developerscripttools._run_abjdev:_run_abjdev',
        ]},
    )
