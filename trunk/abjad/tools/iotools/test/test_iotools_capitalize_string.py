from abjad import *


def test_iotools_capitalize_string_01():

    string = 'violin I'
    assert iotools.capitalize_string(string) == 'Violin I'
