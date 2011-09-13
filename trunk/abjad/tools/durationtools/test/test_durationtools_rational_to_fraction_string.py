from abjad import *
from abjad.tools import durationtools


def test_durationtools_rational_to_fraction_string_01():

    assert durationtools.rational_to_fraction_string(Fraction(1)) == '1/1'
    assert durationtools.rational_to_fraction_string(Fraction(1, 2)) == '1/2'
    assert durationtools.rational_to_fraction_string(Fraction(1, 4)) == '1/4'
    assert durationtools.rational_to_fraction_string(Fraction(2)) == '2/1'
    assert durationtools.rational_to_fraction_string(Fraction(2, 2)) == '1/1'
    assert durationtools.rational_to_fraction_string(Fraction(2, 4)) == '1/2'
    assert durationtools.rational_to_fraction_string(Fraction(-3)) == '-3/1'
    assert durationtools.rational_to_fraction_string(Fraction(-4)) == '-4/1'
