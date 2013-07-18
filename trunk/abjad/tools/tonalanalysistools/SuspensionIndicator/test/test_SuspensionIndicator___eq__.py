from abjad import *
from abjad.tools import tonalanalysistools


def test_SuspensionIndicator___eq___01():

    t = tonalanalysistools.SuspensionIndicator(4, 3)
    u = tonalanalysistools.SuspensionIndicator(4, 3)
    v = tonalanalysistools.SuspensionIndicator(2, 1)

    assert      t == t
    assert      t == u
    assert not t == v

    assert      u == t
    assert      u == u
    assert not u == v

    assert not v == t
    assert not v == u
    assert      v == v
