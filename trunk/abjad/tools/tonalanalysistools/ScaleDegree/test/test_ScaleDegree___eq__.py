# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_ScaleDegree___eq___01():

    scale_degree = tonalanalysistools.ScaleDegree(2)
    u = tonalanalysistools.ScaleDegree(2)
    v = tonalanalysistools.ScaleDegree(3)

    assert      scale_degree == scale_degree
    assert      scale_degree == u
    assert not scale_degree == v

    assert      u == scale_degree
    assert      u == u
    assert not u == v

    assert not v == scale_degree
    assert not v == u
    assert      v == v
