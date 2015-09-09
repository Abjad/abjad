# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_repeat_elements_01():

    sequence_2 = list(sequencetools.repeat_elements(
        list(range(10)), [6, 7, 8], total=3))
    assert sequence_2 == [0, 1, 2, 3, 4, 5, [6, 6, 6], [7, 7, 7], [8, 8, 8], 9]


def test_sequencetools_repeat_elements_02():
    r'''Boundary cases.
    '''

    sequence_2 = list(sequencetools.repeat_elements(
        list(range(10)), [], total=99))
    assert sequence_2 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    sequence_2 = list(sequencetools.repeat_elements(
        list(range(10)), list(range(10)), total=1))
    assert sequence_2 == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]

    sequence_2 = list(sequencetools.repeat_elements(
        list(range(10)), list(range(10)), total=2))
    assert sequence_2 == [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4],
        [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

    sequence_2 = list(sequencetools.repeat_elements(
        list(range(10)), [6, 7, 8], total=0))
    assert sequence_2 == [0, 1, 2, 3, 4, 5, [], [], [], 9]
