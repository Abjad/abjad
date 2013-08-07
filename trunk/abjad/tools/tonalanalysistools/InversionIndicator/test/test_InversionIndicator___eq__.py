# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_InversionIndicator___eq___01():

    inversion_indicator = tonalanalysistools.InversionIndicator(0)
    u = tonalanalysistools.InversionIndicator(0)
    voice = tonalanalysistools.InversionIndicator(1)

    assert      inversion_indicator == inversion_indicator
    assert      inversion_indicator == u
    assert not inversion_indicator == voice

    assert      u == inversion_indicator
    assert      u == u
    assert not u == voice

    assert not voice == inversion_indicator
    assert not voice == u
    assert      voice == voice
