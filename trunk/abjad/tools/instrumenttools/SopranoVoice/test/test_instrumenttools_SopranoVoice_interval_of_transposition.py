from abjad import *


def test_instrumenttools_SopranoVoice_interval_of_transposition_01():

    voice = instrumenttools.SopranoVoice()

    assert voice.interval_of_transposition == pitchtools.MelodicDiatonicInterval('P1')
