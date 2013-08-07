# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_ExtentIndicator___eq___01():

    extent_indicator = tonalanalysistools.ExtentIndicator(5)
    u = tonalanalysistools.ExtentIndicator(5)
    voice = tonalanalysistools.ExtentIndicator(7)

    assert      extent_indicator == extent_indicator
    assert      extent_indicator == u
    assert not extent_indicator == voice

    assert      u == extent_indicator
    assert      u == u
    assert not u == voice

    assert not voice == extent_indicator
    assert not voice == u
    assert      voice == voice
