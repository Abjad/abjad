# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_repeat_sequence_elements_at_indices_01():
    r'''Excepted case.
    '''

    sequence_2 = list(sequencetools.repeat_sequence_elements_at_indices(range(10), [6, 7, 8], 3))
    assert sequence_2 == [0, 1, 2, 3, 4, 5, [6, 6, 6], [7, 7, 7], [8, 8, 8], 9]


def test_sequencetools_repeat_sequence_elements_at_indices_02():
    r'''Boundary cases.
    '''

    sequence_2 = list(sequencetools.repeat_sequence_elements_at_indices(range(10), [], 99))
    assert sequence_2 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    sequence_2 = list(sequencetools.repeat_sequence_elements_at_indices(range(10), range(10), 1))
    assert sequence_2 == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]

    sequence_2 = list(sequencetools.repeat_sequence_elements_at_indices(range(10), range(10), 2))
    assert sequence_2 == [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4],
        [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

    sequence_2 = list(sequencetools.repeat_sequence_elements_at_indices(range(10), [6, 7, 8], 0))
    assert sequence_2 == [0, 1, 2, 3, 4, 5, [], [], [], 9]
