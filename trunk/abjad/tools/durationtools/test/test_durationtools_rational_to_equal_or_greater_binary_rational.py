from abjad import *
from abjad.tools import durationtools


def test_durationtools_rational_to_equal_or_greater_binary_rational_01():
    '''Return least written duration of the form 1 / 2 ** n, such that
        written duration is greater than or equal to prolated duration.'''

    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(1, 80)) == Fraction(1, 64)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(2, 80)) == Fraction(1, 32)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(3, 80)) == Fraction(1, 16)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(4, 80)) == Fraction(1, 16)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(5, 80)) == Fraction(1, 16)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(6, 80)) == Fraction(1, 8)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(7, 80)) == Fraction(1, 8)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(8, 80)) == Fraction(1, 8)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(9, 80)) == Fraction(1, 8)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(10, 80)) == Fraction(1, 8)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(11, 80)) == Fraction(1, 4)
    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(12, 80)) == Fraction(1, 4)


def test_durationtools_rational_to_equal_or_greater_binary_rational_02():
    '''Works for input greater than 1.
    '''

    assert durationtools.rational_to_equal_or_greater_binary_rational(
        Fraction(17, 16)) == Fraction(2, 1)
