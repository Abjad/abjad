# -*- encoding: utf-8 -*-
import itertools


def yield_all_permutations_of_sequence(sequence):
    '''Yields all permutations of `sequence`.

    ::

        >>> list(sequencetools.yield_all_permutations_of_sequence((1, 2, 3)))
        [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

    Returns permutations in lex order.

    Returns generator of `sequence` objects.
    '''
    from abjad.tools import sequencetools

    for permutation in itertools.permutations(range(len(sequence))):
        yield sequencetools.permute_sequence(sequence, permutation)
