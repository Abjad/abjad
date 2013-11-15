# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Suspension___eq___01():

    suspension_indicator = tonalanalysistools.Suspension(4, 3)
    u = tonalanalysistools.Suspension(4, 3)
    voice = tonalanalysistools.Suspension(2, 1)

    assert      suspension_indicator == suspension_indicator
    assert      suspension_indicator == u
    assert not suspension_indicator == voice

    assert      u == suspension_indicator
    assert      u == u
    assert not u == voice

    assert not voice == suspension_indicator
    assert not voice == u
    assert      voice == voice
