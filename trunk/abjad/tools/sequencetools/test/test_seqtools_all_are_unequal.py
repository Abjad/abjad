from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_all_are_unequal_01():
    '''True when the elements in input iterable are unique.'''

    assert sequencetools.all_are_unequal([1, 2, 3])


def test_sequencetools_all_are_unequal_02():
    '''False when the elements in input iterable are not unique.'''

    assert not sequencetools.all_are_unequal([1, 1, 1, 2, 3])


def test_sequencetools_all_are_unequal_03():
    '''False when expr is not a sequence.
    '''

    assert not sequencetools.all_are_unequal(17)
