# -*- coding: utf-8 -*-
from abjad import *


def test_stringtools_capitalize_start_01():

    string = 'violin I'
    assert stringtools.capitalize_start(string) == 'Violin I'


def test_stringtools_capitalize_start_02():
    r'''Length-zero string returns unchanged.
    '''

    assert stringtools.capitalize_start('') == ''
