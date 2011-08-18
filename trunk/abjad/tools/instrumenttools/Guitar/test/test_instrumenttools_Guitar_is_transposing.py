from abjad import *


def test_instrumenttools_Guitar_is_transposing_01():

    guitar = instrumenttools.Guitar()

    assert guitar.is_transposing
