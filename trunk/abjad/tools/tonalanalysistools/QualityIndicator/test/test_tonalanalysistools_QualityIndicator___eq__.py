# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_QualityIndicator___eq___01():

    quality_indicator = tonalanalysistools.QualityIndicator('major')
    u = tonalanalysistools.QualityIndicator('major')
    voice = tonalanalysistools.QualityIndicator('minor')

    assert      quality_indicator == quality_indicator
    assert      quality_indicator == u
    assert not quality_indicator == voice

    assert      u == quality_indicator
    assert      u == u
    assert not u == voice

    assert not voice == quality_indicator
    assert not voice == u
    assert      voice == voice
