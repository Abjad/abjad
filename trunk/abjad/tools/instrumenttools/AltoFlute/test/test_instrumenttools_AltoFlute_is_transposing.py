from abjad import *


def test_instrumenttools_AltoFlute_is_transposing_01():

    alto_flute = instrumenttools.AltoFlute()

    assert alto_flute.is_transposing
