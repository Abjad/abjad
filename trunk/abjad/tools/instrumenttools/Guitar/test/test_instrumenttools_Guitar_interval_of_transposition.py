from abjad import *


def test_instrumenttools_Guitar_interval_of_transposition_01():

    guitar = instrumenttools.Guitar()

    assert guitar.interval_of_transposition == pitchtools.MelodicDiatonicInterval('-P8')
