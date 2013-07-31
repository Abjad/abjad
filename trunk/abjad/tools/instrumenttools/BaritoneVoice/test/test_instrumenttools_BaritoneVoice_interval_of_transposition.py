# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_BaritoneVoice_interval_of_transposition_01():

    voice = instrumenttools.BaritoneVoice()

    assert voice.interval_of_transposition == pitchtools.MelodicDiatonicInterval('P1')
