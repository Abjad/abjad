from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_all_are_nonnegative_integer_equivalent_numbers_01():

    assert sequencetools.all_are_nonnegative_integer_equivalent_numbers([0, 0.0, Fraction(0)])
    assert sequencetools.all_are_nonnegative_integer_equivalent_numbers([2, 3, Fraction(4)])


def test_sequencetools_all_are_nonnegative_integer_equivalent_numbers_02():

    assert not sequencetools.all_are_nonnegative_integer_equivalent_numbers([-1, -2.0, Fraction(-3)])
