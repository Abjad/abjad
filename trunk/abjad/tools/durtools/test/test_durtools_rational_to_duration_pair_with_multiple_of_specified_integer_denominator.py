from abjad import *
from abjad.tools import durtools


def test_durtools_rational_to_duration_pair_with_multiple_of_specified_integer_denominator_01( ):

    duration = Fraction(1, 2)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 2) == (1, 2)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 4) == (2, 4)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 8) == (4, 8)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 16) == (8, 16)


def test_durtools_rational_to_duration_pair_with_multiple_of_specified_integer_denominator_02( ):

    duration = Fraction(1, 2)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 3) == (3, 6)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 6) == (3, 6)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 12) == (6, 12)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 24) == (12, 24)


def test_durtools_rational_to_duration_pair_with_multiple_of_specified_integer_denominator_03( ):

    duration = Fraction(1, 2)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 5) == (5, 10)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 10) == (5, 10)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 20) == (10, 20)
    assert durtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 40) == (20, 40)

