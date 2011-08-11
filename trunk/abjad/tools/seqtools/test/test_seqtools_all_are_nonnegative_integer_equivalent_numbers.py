from abjad import *
from abjad.tools import seqtools


def test_seqtools_all_are_nonnegative_integer_equivalent_numbers_01( ):

    assert seqtools.all_are_nonnegative_integer_equivalent_numbers([0, 0.0, Fraction(0)])
    assert seqtools.all_are_nonnegative_integer_equivalent_numbers([2, 3, Fraction(4)])


def test_seqtools_all_are_nonnegative_integer_equivalent_numbers_02( ):

    assert not seqtools.all_are_nonnegative_integer_equivalent_numbers([-1, -2.0, Fraction(-3)])
