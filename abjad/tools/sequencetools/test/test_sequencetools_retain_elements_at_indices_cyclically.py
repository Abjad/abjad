# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_retain_elements_at_indices_cyclically_01():

    sequence_2 = sequencetools.retain_elements_at_indices_cyclically(range(20), [0, 1], 5)
    assert sequence_2 == [0, 1, 5, 6, 10, 11, 15, 16]


def test_sequencetools_retain_elements_at_indices_cyclically_02():

    sequence_2 = sequencetools.retain_elements_at_indices_cyclically(range(20), [0, 1], 5, 1)
    assert sequence_2 == [1, 2, 6, 7, 11, 12, 16, 17]
