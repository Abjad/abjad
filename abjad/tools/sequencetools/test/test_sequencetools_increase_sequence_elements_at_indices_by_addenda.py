# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_increase_sequence_elements_at_indices_by_addenda_01():
    r'''Increase elements of list sequence_1 by the elements of addenda
    at indices in sequence_1.
    '''

    sequence_1 = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
    sequence_2 = sequencetools.increase_sequence_elements_at_indices_by_addenda(sequence_1, [0.5, 0.5], [0, 4, 8])
    assert sequence_2 == [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]
