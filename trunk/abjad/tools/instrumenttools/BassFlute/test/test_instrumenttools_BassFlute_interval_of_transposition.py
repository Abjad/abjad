from abjad import *


def test_instrumenttools_BassFlute_interval_of_transposition_01():

    bass_flute = instrumenttools.BassFlute()

    assert bass_flute.interval_of_transposition == pitchtools.MelodicDiatonicInterval('-P8')
