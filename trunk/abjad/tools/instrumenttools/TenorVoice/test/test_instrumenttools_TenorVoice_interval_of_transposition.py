from abjad import *


def test_instrumenttools_TenorVoice_interval_of_transposition_01():

    voice = instrumenttools.TenorVoice()

    assert voice.interval_of_transposition == pitchtools.MelodicDiatonicInterval('P1')
