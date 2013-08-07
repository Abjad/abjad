# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_QualityIndicator___eq___01():

    quality_indicator = tonalanalysistools.QualityIndicator('major')
    u = tonalanalysistools.QualityIndicator('major')
    v = tonalanalysistools.QualityIndicator('minor')

    assert      quality_indicator == quality_indicator
    assert      quality_indicator == u
    assert not quality_indicator == v

    assert      u == quality_indicator
    assert      u == u
    assert not u == v

    assert not v == quality_indicator
    assert not v == u
    assert      v == v
