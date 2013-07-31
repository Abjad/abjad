# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_ScaleDegree___eq___01():

    t = tonalanalysistools.ScaleDegree(2)
    u = tonalanalysistools.ScaleDegree(2)
    v = tonalanalysistools.ScaleDegree(3)

    assert      t == t
    assert      t == u
    assert not t == v

    assert      u == t
    assert      u == u
    assert not u == v

    assert not v == t
    assert not v == u
    assert      v == v
