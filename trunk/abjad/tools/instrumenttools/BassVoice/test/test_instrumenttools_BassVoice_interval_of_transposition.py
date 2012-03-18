from abjad import *


def test_instrumenttools_BassVoice_interval_of_transposition_01():

    voice = instrumenttools.BassVoice()

    assert voice.interval_of_transposition == pitchtools.MelodicDiatonicInterval('P1')
