from abjad import *


def test_instrumenttools_Flute_interval_of_transposition_01():

    flute = instrumenttools.Flute()

    assert flute.interval_of_transposition == pitchtools.MelodicDiatonicInterval('P1')
