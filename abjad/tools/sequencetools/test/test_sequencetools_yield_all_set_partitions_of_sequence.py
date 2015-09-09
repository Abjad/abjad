# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_yield_all_set_partitions_of_sequence_01():

    l = [1, 2, 3, 4]
    set_partitions = sequencetools.yield_all_set_partitions_of_sequence(l)

    assert next(set_partitions) == [[1, 2, 3, 4]]
    assert next(set_partitions) == [[1, 2, 3], [4]]
    assert next(set_partitions) == [[1, 2, 4], [3]]
    assert next(set_partitions) == [[1, 2], [3, 4]]
    assert next(set_partitions) == [[1, 2], [3], [4]]
    assert next(set_partitions) == [[1, 3, 4], [2]]
    assert next(set_partitions) == [[1, 3], [2, 4]]
    assert next(set_partitions) == [[1, 3], [2], [4]]
    assert next(set_partitions) == [[1, 4], [2, 3]]
    assert next(set_partitions) == [[1], [2, 3, 4]]
    assert next(set_partitions) == [[1], [2, 3], [4]]
    assert next(set_partitions) == [[1, 4], [2], [3]]
    assert next(set_partitions) == [[1], [2, 4], [3]]
    assert next(set_partitions) == [[1], [2], [3, 4]]
    assert next(set_partitions) == [[1], [2], [3], [4]]
