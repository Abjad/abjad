from abjad import *
from abjad.tools import tonalanalysistools


def test_TonalFunction___eq___01():

    t = tonalanalysistools.TonalFunction(5, 'dominant', 7, 0)
    u = tonalanalysistools.TonalFunction(5, 'dominant', 7, 0, (4, 3))
    v = tonalanalysistools.TonalFunction(5, 'dominant', 7, 0, (4, 3))

    assert      t == t
    assert not t == u
    assert not t == v

    assert not u == t
    assert      u == u
    assert      u == v

    assert not v == t
    assert      v == u
    assert      v == v
