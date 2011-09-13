from abjad import *
from abjad.tools import durationtools


def test_durationtools_rational_to_equal_or_lesser_binary_rational_01():
    '''Return greatest written duration of the form 1 / 2 ** n, such that
    written duration is less than or equal to prolated duration.
    '''

    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(1, 80)) == Fraction(1, 128)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(2, 80)) == Fraction(1, 64)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(3, 80)) == Fraction(1, 32)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(4, 80)) == Fraction(1, 32)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(5, 80)) == Fraction(1, 16)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(6, 80)) == Fraction(1, 16)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(7, 80)) == Fraction(1, 16)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(8, 80)) == Fraction(1, 16)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(9, 80)) == Fraction(1, 16)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(10, 80)) == Fraction(1, 8)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(11, 80)) == Fraction(1, 8)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(
        Fraction(12, 80)) == Fraction(1, 8)


def test_durationtools_rational_to_equal_or_lesser_binary_rational_02():
    '''Return greatest written duration of the form 1 / 2 ** n, such that
    written duration is less than or equal to prolated duration.
    '''

    assert durationtools.rational_to_equal_or_lesser_binary_rational(Fraction(1, 1)) == Fraction(1, 1)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(Fraction(3, 2)) == Fraction(1, 1)

    assert durationtools.rational_to_equal_or_lesser_binary_rational(Fraction(2, 1)) == Fraction(2, 1)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(Fraction(3, 1)) == Fraction(2, 1)

    assert durationtools.rational_to_equal_or_lesser_binary_rational(Fraction(4, 1)) == Fraction(4, 1)
    assert durationtools.rational_to_equal_or_lesser_binary_rational(Fraction(5, 1)) == Fraction(4, 1)
