from abjad import *
from abjad.tools import durationtools


def test_durationtools_rational_to_proper_fraction_01():

    assert durationtools.rational_to_proper_fraction(Fraction(5, 5)) == (1, 0)
    assert durationtools.rational_to_proper_fraction(Fraction(6, 5)) == (1, Fraction(1, 5))
    assert durationtools.rational_to_proper_fraction(Fraction(7, 5)) == (1, Fraction(2, 5))
    assert durationtools.rational_to_proper_fraction(Fraction(8, 5)) == (1, Fraction(3, 5))
    assert durationtools.rational_to_proper_fraction(Fraction(9, 5)) == (1, Fraction(4, 5))

    assert durationtools.rational_to_proper_fraction(Fraction(10, 5)) == (2, 0)
    assert durationtools.rational_to_proper_fraction(Fraction(11, 5)) == (2, Fraction(1, 5))
    assert durationtools.rational_to_proper_fraction(Fraction(12, 5)) == (2, Fraction(2, 5))
    assert durationtools.rational_to_proper_fraction(Fraction(13, 5)) == (2, Fraction(3, 5))
    assert durationtools.rational_to_proper_fraction(Fraction(14, 5)) == (2, Fraction(4, 5))
