from abjad import *
from abjad.tools import durationtools


def test_durationtools_multiply_duration_pair_01():
    t = durationtools.multiply_duration_pair((4, 8), Fraction(4, 5))
    assert t == (16, 40)


def test_durationtools_multiply_duration_pair_02():
    t = durationtools.multiply_duration_pair((4, 8), Fraction(3, 4))
    assert t == (12, 32)
