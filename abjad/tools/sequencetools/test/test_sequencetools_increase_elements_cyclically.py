# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_increase_elements_cyclically_01():

    sequence_1 = range(10)
    sequence_2 = sequencetools.increase_elements_cyclically(sequence_1, [2, 0])
    assert sequence_2 == [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]
