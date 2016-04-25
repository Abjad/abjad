# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_partition_sequence_by_value_of_elements_01():

    sequence_1 = []

    sequence_2 = list(sequencetools.partition_sequence_by_value_of_elements(sequence_1))
    assert sequence_2 == []


def test_sequencetools_partition_sequence_by_value_of_elements_02():

    sequence_1 = [1, 1, 1, 'a', 'a']

    sequence_2 = list(sequencetools.partition_sequence_by_value_of_elements(sequence_1))
    assert sequence_2 == [(1, 1, 1), ('a', 'a')]


def test_sequencetools_partition_sequence_by_value_of_elements_03():

    sequence_1 = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]

    sequence_2 = list(sequencetools.partition_sequence_by_value_of_elements(sequence_1))
    assert sequence_2 == [(0, 0), (-1, -1), (2,), (3,), (-5,), (1, 1), (5,), (-5,)]
