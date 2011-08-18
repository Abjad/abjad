from abjad import *
from abjad.tools import tonalitytools


def test_ExtentIndicator___eq___01():

    t = tonalitytools.ExtentIndicator(5)
    u = tonalitytools.ExtentIndicator(5)
    v = tonalitytools.ExtentIndicator(7)

    assert      t == t
    assert      t == u
    assert not t == v

    assert      u == t
    assert      u == u
    assert not u == v

    assert not v == t
    assert not v == u
    assert      v == v
