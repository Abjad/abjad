# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_yield_all_permutations_of_sequence_in_orbit_01():
    r'''Yield all permutations of tuple in orbit of permutation.
    '''

    generator = sequencetools.yield_all_permutations_of_sequence_in_orbit((1, 2, 3, 4), [1, 2, 3, 0])
    permutations = list(generator)
    assert permutations == [(1, 2, 3, 4), (2, 3, 4, 1), (3, 4, 1, 2), (4, 1, 2, 3)]
