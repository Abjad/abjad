from abjad import *


def test_instrumenttools_BassFlute_is_transposing_01():

    bass_flute = instrumenttools.BassFlute()

    assert bass_flute.is_transposing
