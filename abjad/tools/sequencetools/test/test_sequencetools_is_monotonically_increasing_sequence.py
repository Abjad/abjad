# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_is_monotonically_increasing_sequence_01():
    r'''Is true when the elements in l increase monotonically.
    '''

    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert sequencetools.is_monotonically_increasing_sequence(l)

    l = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
    assert sequencetools.is_monotonically_increasing_sequence(l)


def test_sequencetools_is_monotonically_increasing_sequence_02():
    r'''False when the elements in l do not increase monotonically.
    '''

    l = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert not sequencetools.is_monotonically_increasing_sequence(l)

    l = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
    assert not sequencetools.is_monotonically_increasing_sequence(l)


def test_sequencetools_is_monotonically_increasing_sequence_03():
    r'''Is true when l is empty.
    '''

    l = []
    assert sequencetools.is_monotonically_increasing_sequence(l)
