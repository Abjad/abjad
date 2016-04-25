# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_iterate_sequence_nwise_01():

    sequence_2 = list(sequencetools.iterate_sequence_nwise(range(10), 3))
    assert sequence_2 == [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5),
        (4, 5, 6), (5, 6, 7), (6, 7, 8), (7, 8, 9)]


def test_sequencetools_iterate_sequence_nwise_02():
    r'''Empty iterable boundary case.
    '''

    empty = list(sequencetools.iterate_sequence_nwise([], 3))
    assert empty == []


def test_sequencetools_iterate_sequence_nwise_03():
    r'''Length-1 boundary case.
    '''

    sequence_2 = list(sequencetools.iterate_sequence_nwise(range(10), 1))
    assert sequence_2 == [(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)]
