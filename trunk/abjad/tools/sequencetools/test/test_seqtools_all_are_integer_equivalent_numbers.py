from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_all_are_integer_equivalent_numbers_01():

    assert sequencetools.all_are_integer_equivalent_numbers([1, 2, 3.0, Fraction(4)])


def test_sequencetools_all_are_integer_equivalent_numbers_02():

    assert not sequencetools.all_are_integer_equivalent_numbers([1, 2, 3.5, 4])
    assert not sequencetools.all_are_integer_equivalent_numbers([1, 2, 3, Fraction(4, 11)])
    assert not sequencetools.all_are_integer_equivalent_numbers(7)
    assert not sequencetools.all_are_integer_equivalent_numbers('foo')
