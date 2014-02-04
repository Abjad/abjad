# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_all_are_unequal_01():
    r'''Is true when the elements in input iterable are unique.
    '''

    assert sequencetools.all_are_unequal([1, 2, 3])


def test_sequencetools_all_are_unequal_02():
    r'''False when the elements in input iterable are not unique.
    '''

    assert not sequencetools.all_are_unequal([1, 1, 1, 2, 3])


def test_sequencetools_all_are_unequal_03():
    r'''False when expr is not a sequence.
    '''

    assert not sequencetools.all_are_unequal(17)
