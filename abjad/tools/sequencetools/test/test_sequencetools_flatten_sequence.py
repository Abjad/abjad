# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_sequencetools_flatten_sequence_01():

    l = [1, 2, 3, 4, 5]
    new = sequencetools.flatten_sequence(l)
    assert new == [1, 2, 3, 4, 5]


def test_sequencetools_flatten_sequence_02():

    l = [(1, 2), [3, 4]]
    new = sequencetools.flatten_sequence(l)
    assert new == [1, 2, 3, 4]


def test_sequencetools_flatten_sequence_03():

    l = [(1, 2), [3, (4, 5)]]
    new = sequencetools.flatten_sequence(l)
    assert new == [1, 2, 3, 4, 5]


def test_sequencetools_flatten_sequence_04():

    l = [(1, 2), [3, (4, 5)]]
    new = sequencetools.flatten_sequence(l, classes=(list, ))
    assert new == [(1, 2), 3, (4, 5)]


def test_sequencetools_flatten_sequence_05():

    l = [1, [2, 3, [4]], 5, [6, 7, [8]]]
    assert sequencetools.flatten_sequence(l, depth=0) == \
        [1, [2, 3, [4]], 5, [6, 7, [8]]]
    assert sequencetools.flatten_sequence(l, depth=1) == \
        [1, 2, 3, [4], 5, 6, 7, [8]]
    assert sequencetools.flatten_sequence(l, depth=2) == \
        [1, 2, 3, 4, 5, 6, 7, 8]
    assert sequencetools.flatten_sequence(l, depth=2) == \
        sequencetools.flatten_sequence(l, depth=99)


def test_sequencetools_flatten_sequence_06():
    r'''Works with positive indices.
    '''

    sequence_1 = [0, 1, [2, 3, 4], [5, 6, 7]]
    sequence_2 = sequencetools.flatten_sequence(sequence_1, indices=[2])

    assert sequence_2 == [0, 1, 2, 3, 4, [5, 6, 7]]


def test_sequencetools_flatten_sequence_07():
    r'''Works with negative indices.
    '''

    sequence_1 = [0, 1, [2, 3, 4], [5, 6, 7]]
    works = sequencetools.flatten_sequence(sequence_1, indices=[-1])

    assert works == [0, 1, [2, 3, 4], 5, 6, 7]


def test_sequencetools_flatten_sequence_08():
    r'''Boundary cases.
    '''

    sequence_1 = [0, 1, [2, 3, 4], [5, 6, 7]]

    sequence_2 = sequencetools.flatten_sequence(sequence_1, indices=[])
    assert sequence_2 == [0, 1, [2, 3, 4], [5, 6, 7]]

    sequence_2 = sequencetools.flatten_sequence(sequence_1, indices=[99])
    assert sequence_2 == [0, 1, [2, 3, 4], [5, 6, 7]]

    sequence_2 = sequencetools.flatten_sequence(sequence_1, indices=[-99])
    assert sequence_2 == [0, 1, [2, 3, 4], [5, 6, 7]]
