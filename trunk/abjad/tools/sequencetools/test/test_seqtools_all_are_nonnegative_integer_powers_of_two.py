from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_all_are_nonnegative_integer_powers_of_two_01():
    '''True when all elements in sequence are nonnegative integer powers of two.
    '''

    assert sequencetools.all_are_nonnegative_integer_powers_of_two([1, 2, 256, 8, 16, 16, 16])


def test_sequencetools_all_are_nonnegative_integer_powers_of_two_02():
    '''True on empty sequence.
    '''

    assert sequencetools.all_are_nonnegative_integer_powers_of_two([])


def test_sequencetools_all_are_nonnegative_integer_powers_of_two_03():
    '''False otherwise.
    '''

    assert not sequencetools.all_are_nonnegative_integer_powers_of_two([3])
    assert not sequencetools.all_are_nonnegative_integer_powers_of_two([1, 2, 4, 8, 16, 17])


def test_sequencetools_all_are_nonnegative_integer_powers_of_two_04():
    '''False when expr is not a sequence.
    '''

    assert not sequencetools.all_are_nonnegative_integer_powers_of_two(16)
