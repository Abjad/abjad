from abjad import *
from abjad.tools import durationtools


def test_durationtools_is_duration_pair_01():

    assert durationtools.is_duration_pair((1, 4))
    assert not durationtools.is_duration_pair((1, 2, 3, 4))
    assert not durationtools.is_duration_pair(Fraction(1, 4))
    assert not durationtools.is_duration_pair([(1, 4)])
    assert not durationtools.is_duration_pair([Fraction(1, 4)])
