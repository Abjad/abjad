from abjad import *
from abjad.tools import durationtools


def test_durationtools_rational_to_duration_pair_with_multiple_of_specified_integer_denominator_01():

    duration = Fraction(1, 2)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 2) == (1, 2)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 4) == (2, 4)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 8) == (4, 8)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 16) == (8, 16)


def test_durationtools_rational_to_duration_pair_with_multiple_of_specified_integer_denominator_02():

    duration = Fraction(1, 2)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 3) == (3, 6)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 6) == (3, 6)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 12) == (6, 12)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 24) == (12, 24)


def test_durationtools_rational_to_duration_pair_with_multiple_of_specified_integer_denominator_03():

    duration = Fraction(1, 2)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 5) == (5, 10)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 10) == (5, 10)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 20) == (10, 20)
    assert durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, 40) == (20, 40)
