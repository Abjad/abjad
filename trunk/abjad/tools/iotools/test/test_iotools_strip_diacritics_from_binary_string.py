from abjad import *


def test_iotools_strip_diacritics_from_binary_string_01():

    binary_string = 'Dvo\xc5\x99\xc3\xa1k'
    ascii_string = iotools.strip_diacritics_from_binary_string(binary_string)

    assert ascii_string == 'Dvorak'
