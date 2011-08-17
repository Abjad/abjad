#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from distutils.core import setup
from ez_setup import use_setuptools
use_setuptools( ) ### this must come before setup import
from setuptools import setup, find_packages

setup(name = 'Abjad', 
    version = '2.0',
    description = 'Abjad is a Python API for Formalized Score Control.',
    long_description = 'Abjad is an interactive software system designed to help composers build up complex pieces of music notation in an iterative and incremental way. Use Abjad to create a symbolic representation of all the notes, rests, staves, tuplets, beams and slurs in any score. Because Abjad extends the Python programming language, you can use Abjad to make systematic changes to your music as you work. And because Abjad wraps the powerful LilyPond music notation package, you can use Abjad to control the typographic details of all the symbols on the page.',
    author = 'Victor Adan and Trevor Baca',
    author_email = 'contact@victoradan.net, trevorbaca@gmail.com',
    url = 'http://www.projectabjad.org',
    keywords = 'music composition, music notation, formalized score control, lilypond',
    license = 'GPL',
    platforms = 'All',
    packages = find_packages( ), ### include all packages found in '.'
    #scripts = ['ez_setup.py'],
    include_package_data = True, ### include all file types under abjad.
    entry_points = { 'console_scripts':[
        'abj = abjad.tools.iotools._run_abjad:_run_abjad',
        'abjad = abjad.tools.iotools._run_abjad:_run_abjad',
        'abjad-book = abjad.book.abjad_book:_abjad_book',
        ] },
     )
