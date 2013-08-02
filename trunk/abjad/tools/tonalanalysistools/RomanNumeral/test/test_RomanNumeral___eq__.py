# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_RomanNumeral___eq___01():

    t = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0)
    u = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0, (4, 3))
    v = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0, (4, 3))

    assert      t == t
    assert not t == u
    assert not t == v

    assert not u == t
    assert      u == u
    assert      u == v

    assert not v == t
    assert      v == u
    assert      v == v
