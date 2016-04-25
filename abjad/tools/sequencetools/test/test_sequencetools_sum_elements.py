# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_sequencetools_sum_elements_01():
    r'''Sum slices cyclically at every fourth index.
    '''

    sequence_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 1)], period=4)
    assert sequence_2 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 2)], period=4)
    assert sequence_2 == [1, 2, 3, 9, 6, 7, 17, 10, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 3)], period=4)
    assert sequence_2 == [3, 3, 15, 7, 27, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 4)], period=4)
    assert sequence_2 == [6, 22, 38]


def test_sequencetools_sum_elements_02():
    r'''Sum slice at only the zeroth index.
    Append overhang elements.
    '''

    sequence_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 1)])
    assert sequence_2 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 2)])
    assert sequence_2 == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 3)])
    assert sequence_2 == [3, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 4)])
    assert sequence_2 == [6, 4, 5, 6, 7, 8, 9, 10, 11]


def test_sequencetools_sum_elements_03():
    r'''Sum every 5, 6, 7 or 8 elements together.
    Do append incomplete final sums.
    '''

    sequence_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 5)], period=5, overhang=True)
    assert sequence_2 == [10, 35, 21]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 6)], period=6, overhang=True)
    assert sequence_2 == [15, 51]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 7)], period=7, overhang=True)
    assert sequence_2 == [21, 45]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 8)], period=8, overhang=True)
    assert sequence_2 == [28, 38]


def test_sequencetools_sum_elements_04():
    r'''Sum every 5, 6, 7 or 8 elements together.
    Do not append incomplete final sums.
    '''

    sequence_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 5)], period=5, overhang=False)
    assert sequence_2 == [10, 35]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 6)], period=6, overhang=False)
    assert sequence_2 == [15, 51]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 7)], period=7, overhang=False)
    assert sequence_2 == [21]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 8)], period=8, overhang=False)
    assert sequence_2 == [28]


def test_sequencetools_sum_elements_05():
    r'''Sum at multiple points in each period.
    '''

    sequence_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    sequence_2 = sequencetools.sum_elements(sequence_1, [(0, 2), (2, 2)], period=5)
    assert sequence_2 == [1, 5, 4, 11, 15, 9, 21]


def test_sequencetools_sum_elements_06():
    r'''Affected indices must be less than period.
    '''

    sequence_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    statement = 'sequencetools.sum_elements(sequence_1, [(0, 99)], period=4)'
    assert pytest.raises(ValueError, statement)
