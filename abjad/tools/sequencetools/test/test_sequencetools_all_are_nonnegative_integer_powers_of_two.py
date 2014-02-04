# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_all_are_nonnegative_integer_powers_of_two_01():
    r'''Is true when all elements in sequence are nonnegative integer 
    powers of two.
    '''

    numbers = [1, 2, 256, 8, 16, 16, 16]
    assert sequencetools.all_are_nonnegative_integer_powers_of_two(numbers)


def test_sequencetools_all_are_nonnegative_integer_powers_of_two_02():
    r'''True on empty sequence.
    '''

    assert sequencetools.all_are_nonnegative_integer_powers_of_two([])


def test_sequencetools_all_are_nonnegative_integer_powers_of_two_03():
    r'''Otherwise false.
    '''

    assert not sequencetools.all_are_nonnegative_integer_powers_of_two([3])

    numbers = [1, 2, 4, 8, 16, 17]
    assert not sequencetools.all_are_nonnegative_integer_powers_of_two(numbers)


def test_sequencetools_all_are_nonnegative_integer_powers_of_two_04():
    r'''False when expr is not a sequence.
    '''

    assert not sequencetools.all_are_nonnegative_integer_powers_of_two(16)
