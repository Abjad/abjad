# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_increase_sequence_elements_cyclically_by_addenda_01():

    sequence_1 = range(10)
    sequence_2 = sequencetools.increase_sequence_elements_cyclically_by_addenda(sequence_1, [2, 0])
    assert sequence_2 == [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]


def test_sequencetools_increase_sequence_elements_cyclically_by_addenda_02():

    sequence_1 = range(10)
    sequence_2 = sequencetools.increase_sequence_elements_cyclically_by_addenda(sequence_1, [10, -10])
    assert sequence_2 == [10, 1, 12, 1, 14, 1, 16, 1, 18, 1]


def test_sequencetools_increase_sequence_elements_cyclically_by_addenda_03():

    sequence_1 = range(10)
    sequence_2 = sequencetools.increase_sequence_elements_cyclically_by_addenda(sequence_1, [10, -10], shield=False)
    assert sequence_2 == [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]
