# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_all_are_assignable_integers_01():
    r'''Is true when all elements in sequence are all notehead assignable.
    '''

    assert sequencetools.all_are_assignable_integers([1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16])


def test_sequencetools_all_are_assignable_integers_02():
    r'''True on empty sequence.
    '''

    assert sequencetools.all_are_assignable_integers([])


def test_sequencetools_all_are_assignable_integers_03():
    r'''Otherwise false.
    '''

    assert not sequencetools.all_are_assignable_integers([0, 1, 2, 4, 5])


def test_sequencetools_all_are_assignable_integers_04():
    r'''False when expr is not a sequence.
    '''

    assert not sequencetools.all_are_assignable_integers(16)
