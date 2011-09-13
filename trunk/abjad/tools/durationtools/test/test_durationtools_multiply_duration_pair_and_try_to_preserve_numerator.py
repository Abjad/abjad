from abjad import *
from abjad.tools import durationtools


def test_durationtools_multiply_duration_pair_and_try_to_preserve_numerator_01():
    t = durationtools.multiply_duration_pair_and_try_to_preserve_numerator((9, 16), Fraction(2, 3))
    assert t == (9, 24)


def test_durationtools_multiply_duration_pair_and_try_to_preserve_numerator_02():
    t = durationtools.multiply_duration_pair_and_try_to_preserve_numerator((9, 16), Fraction(1, 2))
    assert t == (9, 32)


def test_durationtools_multiply_duration_pair_and_try_to_preserve_numerator_03():
    t = durationtools.multiply_duration_pair_and_try_to_preserve_numerator((9, 16), Fraction(5, 6))
    assert t == (45, 96)


def test_durationtools_multiply_duration_pair_and_try_to_preserve_numerator_04():
    t = durationtools.multiply_duration_pair_and_try_to_preserve_numerator((3, 8), Fraction(2, 3))
    assert t == (3, 12)
