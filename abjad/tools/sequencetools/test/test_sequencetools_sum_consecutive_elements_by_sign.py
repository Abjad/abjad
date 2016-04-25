# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_sum_consecutive_elements_by_sign_01():

    sequence_1 = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    sequence_2 = list(sequencetools.sum_consecutive_elements_by_sign(sequence_1))
    assert sequence_2 == [0, -2, 5, -5, 8, -11]

    sequence_2 = list(sequencetools.sum_consecutive_elements_by_sign(sequence_1, sign=[-1]))
    assert sequence_2 == [0, 0, -2, 2, 3, -5, 1, 2, 5, -11]

    sequence_2 = list(sequencetools.sum_consecutive_elements_by_sign(sequence_1, sign=[0]))
    assert sequence_2 == [0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    sequence_2 = list(sequencetools.sum_consecutive_elements_by_sign(sequence_1, sign=[1]))
    assert sequence_2 == [0, 0, -1, -1, 5, -5, 8, -5, -6]

    sequence_2 = list(sequencetools.sum_consecutive_elements_by_sign(sequence_1, sign=[-1, 0]))
    assert sequence_2 == [0, -2, 2, 3, -5, 1, 2, 5, -11]

    sequence_2 = list(sequencetools.sum_consecutive_elements_by_sign(sequence_1, sign=[-1, 1]))
    assert sequence_2 == [0, 0, -2, 5, -5, 8, -11]

    sequence_2 = list(sequencetools.sum_consecutive_elements_by_sign(sequence_1, sign=[0, 1]))
    assert sequence_2 == [0, -1, -1, 5, -5, 8, -5, -6]

    sequence_2 = list(sequencetools.sum_consecutive_elements_by_sign(sequence_1, sign=[-1, 0, 1]))
    assert sequence_2 == [0, -2, 5, -5, 8, -11]
