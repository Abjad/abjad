# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_splice_new_elements_between_sequence_elements_01():
    r'''Insert a copy of the elements of sequence 2 between
    each of the elements of sequence 1.
    '''

    sequence_1 = [0, 1, 2, 3, 4]
    sequence_2 = ['A', 'B']

    t = sequencetools.splice_new_elements_between_sequence_elements(
        sequence_1, sequence_2)
    assert t == [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

    t = sequencetools.splice_new_elements_between_sequence_elements(
        sequence_1, sequence_2, overhang=(0, 1))
    assert t == [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']

    t = sequencetools.splice_new_elements_between_sequence_elements(
        sequence_1, sequence_2, overhang=(1, 0))
    assert t == ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

    t = sequencetools.splice_new_elements_between_sequence_elements(
        sequence_1, sequence_2, overhang=(1, 1))
    assert t == ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']
