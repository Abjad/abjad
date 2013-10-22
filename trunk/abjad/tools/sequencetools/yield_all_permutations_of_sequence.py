# -*- encoding: utf-8 -*-
from abjad.tools.sequencetools.permute_sequence import permute_sequence
import itertools


def yield_all_permutations_of_sequence(sequence):
    '''Yield all permutations of `sequence` in lex order:

    ::

        >>> list(sequencetools.yield_all_permutations_of_sequence((1, 2, 3)))
        [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

    Returns generator of `sequence` objects.
    '''

    for permutation in itertools.permutations(range(len(sequence))):
        yield permute_sequence(sequence, permutation)
