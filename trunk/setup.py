#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from distutils.core import setup
from ez_setup import use_setuptools
use_setuptools( ) ### this must come before setup import
from setuptools import setup, find_packages

setup(name = 'Abjad', 
      version = '2.0',
      description = 'Abjad is a Python API for Formalized Score Control.',
      long_description = 'Abjad is a Python API for Formalized Score Control.',
      author = 'Victor Adan and Trevor Baca',
      author_email = 'contact@victoradan.net, trevorbaca@gmail.com',
      url = 'http://www.projectabjad.org',
      keywords = 'music formalized score control lilypond composition',
      license = 'GPL',
      packages = find_packages( ), ### include all packages found in '.'
      #scripts = ['ez_setup.py'],
      include_package_data = True, ### include all file types under abjad.
      entry_points = { 'console_scripts':[
         'abj = abjad.tools.iotools._run_abjad:_run_abjad',
         'abjad-book = abjad.book.abjad_book:_abjad_book',
         ] },
      )
