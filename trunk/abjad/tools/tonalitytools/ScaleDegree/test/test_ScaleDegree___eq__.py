from abjad import *
from abjad.tools import tonalitytools


def test_ScaleDegree___eq___01():

    t = tonalitytools.ScaleDegree(2)
    u = tonalitytools.ScaleDegree(2)
    v = tonalitytools.ScaleDegree(3)

    assert      t == t
    assert      t == u
    assert not t == v

    assert      u == t
    assert      u == u
    assert not u == v

    assert not v == t
    assert not v == u
    assert      v == v
