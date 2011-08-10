from abjad import *
from abjad.tools import durtools


def test_durtools_multiply_duration_pair_and_try_to_preserve_numerator_01( ):
    t = durtools.multiply_duration_pair_and_try_to_preserve_numerator((9, 16), Fraction(2, 3))
    assert t == (9, 24)


def test_durtools_multiply_duration_pair_and_try_to_preserve_numerator_02( ):
    t = durtools.multiply_duration_pair_and_try_to_preserve_numerator((9, 16), Fraction(1, 2))
    assert t == (9, 32)


def test_durtools_multiply_duration_pair_and_try_to_preserve_numerator_03( ):
    t = durtools.multiply_duration_pair_and_try_to_preserve_numerator((9, 16), Fraction(5, 6))
    assert t == (45, 96)


def test_durtools_multiply_duration_pair_and_try_to_preserve_numerator_04( ):
    t = durtools.multiply_duration_pair_and_try_to_preserve_numerator((3, 8), Fraction(2, 3))
    assert t == (3, 12)
