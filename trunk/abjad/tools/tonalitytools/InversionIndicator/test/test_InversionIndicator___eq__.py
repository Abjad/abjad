from abjad import *
from abjad.tools import tonalitytools


def test_InversionIndicator___eq___01():

    t = tonalitytools.InversionIndicator(0)
    u = tonalitytools.InversionIndicator(0)
    v = tonalitytools.InversionIndicator(1)

    assert      t == t
    assert      t == u
    assert not t == v

    assert      u == t
    assert      u == u
    assert not u == v

    assert not v == t
    assert not v == u
    assert      v == v
