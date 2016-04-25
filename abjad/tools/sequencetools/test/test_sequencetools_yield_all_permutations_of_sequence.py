# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_yield_all_permutations_of_sequence_01():
    r'''Yield all permtuations of tuple.
    '''

    sequence = (1, 2, 3)
    generator = sequencetools.yield_all_permutations_of_sequence(sequence)
    permutations = list(generator)
    assert permutations == [(1, 2, 3), (1, 3, 2), (2, 1, 3), 
        (2, 3, 1), (3, 1, 2), (3, 2, 1)]
