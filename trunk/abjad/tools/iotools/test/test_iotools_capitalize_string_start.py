from abjad import *


def test_iotools_capitalize_string_start_01():

    string = 'violin I'
    assert iotools.capitalize_string_start(string) == 'Violin I'
