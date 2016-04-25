# -*- coding: utf-8 -*-
import collections
import itertools


def yield_all_permutations_of_sequence(sequence):
    '''Yields all permutations of `sequence`.

    ::

        >>> list(sequencetools.yield_all_permutations_of_sequence((1, 2, 3)))
        [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

    Yields permutations in lex order.

    Returns generator.
    '''
    from abjad.tools import sequencetools

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    for permutation in itertools.permutations(tuple(range(len(sequence)))):
        yield sequencetools.permute_sequence(sequence, permutation)
