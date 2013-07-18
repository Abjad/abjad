from abjad import *
from abjad.tools import tonalanalysistools


def test_ExtentIndicator___eq___01():

    t = tonalanalysistools.ExtentIndicator(5)
    u = tonalanalysistools.ExtentIndicator(5)
    v = tonalanalysistools.ExtentIndicator(7)

    assert      t == t
    assert      t == u
    assert not t == v

    assert      u == t
    assert      u == u
    assert not u == v

    assert not v == t
    assert not v == u
    assert      v == v
