from abjad import *
from abjad.tools import tonalitytools


def test_SuspensionIndicator___eq___01():

    t = tonalitytools.SuspensionIndicator(4, 3)
    u = tonalitytools.SuspensionIndicator(4, 3)
    v = tonalitytools.SuspensionIndicator(2, 1)

    assert      t == t
    assert      t == u
    assert not t == v

    assert      u == t
    assert      u == u
    assert not u == v

    assert not v == t
    assert not v == u
    assert      v == v
