# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_TenorVoice_is_transposing_01():

    voice = instrumenttools.TenorVoice()

    assert not voice.is_transposing
