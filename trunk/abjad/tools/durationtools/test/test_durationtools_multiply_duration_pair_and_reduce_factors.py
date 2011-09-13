from abjad import *
from abjad.tools import durationtools


def test_durationtools_multiply_duration_pair_and_reduce_factors_01():
    assert durationtools.multiply_duration_pair_and_reduce_factors(
        (4, 8), Fraction(2, 3)) == (4, 12)


def test_durationtools_multiply_duration_pair_and_reduce_factors_02():
    assert durationtools.multiply_duration_pair_and_reduce_factors(
        (4, 8), Fraction(4, 1)) == (4, 2)


def test_durationtools_multiply_duration_pair_and_reduce_factors_03():
    assert durationtools.multiply_duration_pair_and_reduce_factors(
        (4, 8), Fraction(3, 5)) == (12, 40)


def test_durationtools_multiply_duration_pair_and_reduce_factors_04():
    assert durationtools.multiply_duration_pair_and_reduce_factors(
        (4, 8), Fraction(6, 5)) == (12, 20)


def test_durationtools_multiply_duration_pair_and_reduce_factors_05():
    assert durationtools.multiply_duration_pair_and_reduce_factors(
        (5, 6), Fraction(6, 5)) == (1, 1)
