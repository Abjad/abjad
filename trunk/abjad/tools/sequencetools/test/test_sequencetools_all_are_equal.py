from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_all_are_equal_01():
    '''True when all elements in sequence are equal.
    '''

    assert sequencetools.all_are_equal([-1, -1, -1, -1, -1])
    assert sequencetools.all_are_equal([0, 0, 0, 0, 0])
    assert sequencetools.all_are_equal([1, 1, 1, 1, 1])
    assert sequencetools.all_are_equal([2, 2, 2, 2, 2])


def test_sequencetools_all_are_equal_02():
    '''True on empty sequence.
    '''

    assert sequencetools.all_are_equal([])


def test_sequencetools_all_are_equal_03():
    '''False otherwise.
    '''

    assert not sequencetools.all_are_equal([-1, -1, -1, -1, 99])
    assert not sequencetools.all_are_equal([0, 0, 0, 0, 99])
    assert not sequencetools.all_are_equal([1, 1, 1, 1, 99])
    assert not sequencetools.all_are_equal([2, 2, 2, 2, 99])


def test_sequencetools_all_are_equal_04():
    '''False when expr is not a sequence.
    '''

    assert not sequencetools.all_are_equal(17)
