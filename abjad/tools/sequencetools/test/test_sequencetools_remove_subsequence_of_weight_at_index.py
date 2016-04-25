# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_remove_subsequence_of_weight_at_index_01():

    sequence_2 = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
    result = sequencetools.remove_subsequence_of_weight_at_index(sequence_2, 8, 0)

    assert result == [4, 5, 1, 2, 5, 5, 6]


def test_sequencetools_remove_subsequence_of_weight_at_index_02():

    sequence_2 = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
    result = sequencetools.remove_subsequence_of_weight_at_index(sequence_2, 13, 4)

    assert result == [1, 1, 2, 3, 5, 5, 6]
