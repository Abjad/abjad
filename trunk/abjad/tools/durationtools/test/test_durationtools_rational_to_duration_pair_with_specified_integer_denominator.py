from abjad import *
from abjad.tools import durationtools


def test_durationtools_rational_to_duration_pair_with_specified_integer_denominator_01():
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((0, 6), 12) == (0, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((1, 6), 12) == (2, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((2, 6), 12) == (4, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((3, 6), 12) == (6, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((4, 6), 12) == (8, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((5, 6), 12) == (10, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((6, 6), 12) == (12, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((7, 6), 12) == (14, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((8, 6), 12) == (16, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((9, 6), 12) == (18, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((10, 6), 12) == (20, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((11, 6), 12) == (22, 12)


def test_durationtools_rational_to_duration_pair_with_specified_integer_denominator_02():
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((0, 12), 6) == (0, 6)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((1, 12), 6) == (1, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((2, 12), 6) == (1, 6)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((3, 12), 6) == (3, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((4, 12), 6) == (2, 6)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((5, 12), 6) == (5, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((6, 12), 6) == (3, 6)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((7, 12), 6) == (7, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((8, 12), 6) == (4, 6)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((9, 12), 6) == (9, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((10, 12), 6) == (5, 6)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((11, 12), 6) == (11, 12)


def test_durationtools_rational_to_duration_pair_with_specified_integer_denominator_03():
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((0, 12), 8) == (0, 8)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((1, 12), 8) == (1, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((2, 12), 8) == (2, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((3, 12), 8) == (2, 8)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((4, 12), 8) == (4, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((5, 12), 8) == (5, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((6, 12), 8) == (4, 8)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((7, 12), 8) == (7, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((8, 12), 8) == (8, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((9, 12), 8) == (6, 8)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((10, 12), 8) == (10, 12)
    assert durationtools.rational_to_duration_pair_with_specified_integer_denominator((11, 12), 8) == (11, 12)
