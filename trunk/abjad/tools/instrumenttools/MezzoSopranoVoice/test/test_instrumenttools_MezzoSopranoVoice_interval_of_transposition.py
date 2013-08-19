# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_MezzoSopranoVoice_interval_of_transposition_01():

    voice = instrumenttools.MezzoSopranoVoice()

    assert voice.interval_of_transposition == pitchtools.NamedMelodicInterval('P1')
