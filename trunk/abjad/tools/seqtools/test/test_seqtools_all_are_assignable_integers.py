from abjad import *
from abjad.tools import seqtools


def test_seqtools_all_are_assignable_integers_01():
    '''True when all elements in sequence are all notehead assignable.
    '''

    assert seqtools.all_are_assignable_integers([1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16])


def test_seqtools_all_are_assignable_integers_02():
    '''True on empty sequence.
    '''

    assert seqtools.all_are_assignable_integers([])


def test_seqtools_all_are_assignable_integers_03():
    '''False otherwise.
    '''

    assert not seqtools.all_are_assignable_integers([0, 1, 2, 4, 5])


def test_seqtools_all_are_assignable_integers_04():
    '''False when expr is not a sequence.'''

    assert not seqtools.all_are_assignable_integers(16)
