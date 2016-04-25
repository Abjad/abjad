# -*- coding: utf-8 -*-
import collections


def yield_all_permutations_of_sequence_in_orbit(sequence, permutation):
    '''Yields all permutations of `sequence` in orbit of `permutation`.

    ::

        >>> list(sequencetools.yield_all_permutations_of_sequence_in_orbit(
        ...     (1, 2, 3, 4), [1, 2, 3, 0]))
        [(1, 2, 3, 4), (2, 3, 4, 1), (3, 4, 1, 2), (4, 1, 2, 3)]

    Yields permutations in lex order.

    Returns generator.
    '''
    from abjad.tools import sequencetools

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    if not sequencetools.Sequence(permutation).is_permutation() or \
        len(sequence) != len(permutation):
        args = (str(permutation), len(sequence))
        message = '{!r} must be permutation of length {}.'
        message = message.format(permutation, len(sequence))
        raise TypeError(message)

    # returns identity first
    next_permutation = sequencetools.permute_sequence(
        sequence, range(len(sequence)))
    yield next_permutation

    # then returns remaining permutations in orbit of permutation
    while True:
        next_permutation = sequencetools.permute_sequence(
            next_permutation, permutation)
        if next_permutation == sequence:
            break
        else:
            yield next_permutation
