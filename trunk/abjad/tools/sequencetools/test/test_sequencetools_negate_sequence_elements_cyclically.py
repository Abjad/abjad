# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_negate_sequence_elements_cyclically_01():

    sequence_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sequence_2 = sequencetools.negate_sequence_elements_cyclically(sequence_1, [0, 1, 2], 5)

    assert sequence_2 == [-1, -2, -3, 4, 5, -6, -7, -8, 9, 10]
