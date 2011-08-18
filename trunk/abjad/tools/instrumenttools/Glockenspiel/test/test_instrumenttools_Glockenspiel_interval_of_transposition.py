from abjad import *


def test_instrumenttools_Glockenspiel_interval_of_transposition_01():

    glockenspiel = instrumenttools.Glockenspiel()

    assert glockenspiel.interval_of_transposition == pitchtools.MelodicDiatonicInterval('+P15')
