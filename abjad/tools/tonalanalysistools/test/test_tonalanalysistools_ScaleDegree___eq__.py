# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree___eq___01():

    scale_degree = tonalanalysistools.ScaleDegree(2)
    u = tonalanalysistools.ScaleDegree(2)
    voice = tonalanalysistools.ScaleDegree(3)

    assert      scale_degree == scale_degree
    assert      scale_degree == u
    assert not scale_degree == voice

    assert      u == scale_degree
    assert      u == u
    assert not u == voice

    assert not voice == scale_degree
    assert not voice == u
    assert      voice == voice
