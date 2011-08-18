from abjad import *


def test_instrumenttools_ContrabassFlute_is_transposing_01():

    contrabass_flute = instrumenttools.ContrabassFlute()

    assert contrabass_flute.is_transposing
