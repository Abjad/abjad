from abjad import *
from abjad.tools import tonalitytools


def test_QualityIndicator___eq___01():

    t = tonalitytools.QualityIndicator('major')
    u = tonalitytools.QualityIndicator('major')
    v = tonalitytools.QualityIndicator('minor')

    assert      t == t
    assert      t == u
    assert not t == v

    assert      u == t
    assert      u == u
    assert not u == v

    assert not v == t
    assert not v == u
    assert      v == v
