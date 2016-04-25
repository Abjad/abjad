# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_increase_elements_01():

    sequence_1 = range(10)
    sequence_2 = sequencetools.increase_elements(sequence_1, [2, 0])
    assert sequence_2 == [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]


def test_sequencetools_increase_elements_02():

    sequence_1 = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
    sequence_2 = sequencetools.increase_elements(
        sequence_1, [0.5, 0.5], indices=[0, 4, 8]
        )
    assert sequence_2 == [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]
