from abjad import *


def test_instrumenttools_Piccolo_interval_of_transposition_01():

    piccolo = instrumenttools.Piccolo()

    piccolo.interval_of_transposition == pitchtools.MelodicDiatonicInterval('+P8')
