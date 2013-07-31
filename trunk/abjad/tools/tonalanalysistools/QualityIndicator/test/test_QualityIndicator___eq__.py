# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_QualityIndicator___eq___01():

    t = tonalanalysistools.QualityIndicator('major')
    u = tonalanalysistools.QualityIndicator('major')
    v = tonalanalysistools.QualityIndicator('minor')

    assert      t == t
    assert      t == u
    assert not t == v

    assert      u == t
    assert      u == u
    assert not u == v

    assert not v == t
    assert not v == u
    assert      v == v
