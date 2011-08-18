from abjad import *


def test_instrumenttools_ContrabassFlute_interval_of_transposition_01():

    contrabass_flute = instrumenttools.ContrabassFlute()

    assert contrabass_flute.interval_of_transposition == pitchtools.MelodicDiatonicInterval('-P11')
