from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_sum_consecutive_sequence_elements_by_sign_01():

    l = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    t = list(sequencetools.sum_consecutive_sequence_elements_by_sign(l))
    assert t == [0, -2, 5, -5, 8, -11]

    t = list(sequencetools.sum_consecutive_sequence_elements_by_sign(l, sign = [-1]))
    assert t == [0, 0, -2, 2, 3, -5, 1, 2, 5, -11]

    t = list(sequencetools.sum_consecutive_sequence_elements_by_sign(l, sign = [0]))
    assert t == [0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    t = list(sequencetools.sum_consecutive_sequence_elements_by_sign(l, sign = [1]))
    assert t == [0, 0, -1, -1, 5, -5, 8, -5, -6]

    t = list(sequencetools.sum_consecutive_sequence_elements_by_sign(l, sign = [-1, 0]))
    assert t == [0, -2, 2, 3, -5, 1, 2, 5, -11]

    t = list(sequencetools.sum_consecutive_sequence_elements_by_sign(l, sign = [-1, 1]))
    assert t == [0, 0, -2, 5, -5, 8, -11]

    t = list(sequencetools.sum_consecutive_sequence_elements_by_sign(l, sign = [0, 1]))
    assert t == [0, -1, -1, 5, -5, 8, -5, -6]

    t = list(sequencetools.sum_consecutive_sequence_elements_by_sign(l, sign = [-1, 0, 1]))
    assert t == [0, -2, 5, -5, 8, -11]
