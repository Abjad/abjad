from abjad import *
from abjad.tools import durationtools


def test_durationtools_rational_to_flag_count_01():

    assert durationtools.rational_to_flag_count(Fraction(1, 64)) == 4
    assert durationtools.rational_to_flag_count(Fraction(2, 64)) == 3
    assert durationtools.rational_to_flag_count(Fraction(3, 64)) == 3
    assert durationtools.rational_to_flag_count(Fraction(4, 64)) == 2
    assert durationtools.rational_to_flag_count(Fraction(5, 64)) == 2
    assert durationtools.rational_to_flag_count(Fraction(6, 64)) == 2
    assert durationtools.rational_to_flag_count(Fraction(7, 64)) == 2
    assert durationtools.rational_to_flag_count(Fraction(8, 64)) == 1
