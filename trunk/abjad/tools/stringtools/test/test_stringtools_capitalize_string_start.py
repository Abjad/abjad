from abjad import *


def test_stringtools_capitalize_string_start_01():

    string = 'violin I'
    assert stringtools.capitalize_string_start(string) == 'Violin I'


def test_stringtools_capitalize_string_start_02():
    '''Length-zero string returns unchanged.
    '''

    assert stringtools.capitalize_string_start('') == ''
