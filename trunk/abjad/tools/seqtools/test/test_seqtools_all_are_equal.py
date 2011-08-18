from abjad import *
from abjad.tools import seqtools


def test_seqtools_all_are_equal_01():
    '''True when all elements in sequence are equal.
    '''

    assert seqtools.all_are_equal([-1, -1, -1, -1, -1])
    assert seqtools.all_are_equal([0, 0, 0, 0, 0])
    assert seqtools.all_are_equal([1, 1, 1, 1, 1])
    assert seqtools.all_are_equal([2, 2, 2, 2, 2])


def test_seqtools_all_are_equal_02():
    '''True on empty sequence.
    '''

    assert seqtools.all_are_equal([ ])


def test_seqtools_all_are_equal_03():
    '''False otherwise.
    '''

    assert not seqtools.all_are_equal([-1, -1, -1, -1, 99])
    assert not seqtools.all_are_equal([0, 0, 0, 0, 99])
    assert not seqtools.all_are_equal([1, 1, 1, 1, 99])
    assert not seqtools.all_are_equal([2, 2, 2, 2, 99])


def test_seqtools_all_are_equal_04():
    '''False when expr is not a sequence.
    '''

    assert not seqtools.all_are_equal(17)
