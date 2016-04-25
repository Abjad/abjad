# -*- coding: utf-8 -*-
import collections


def yield_all_unordered_pairs_of_sequence(sequence):
    '''Yields all unordered pairs of `sequence`.

    ::

        >>> list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 2, 3, 4]))
        [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]

    Yields all unordered pairs of length-``1`` `sequence`:

    ::

        >>> list(sequencetools.yield_all_unordered_pairs_of_sequence([1]))
        []

    Yields all unordered pairs of empty `sequence`:

    ::

        >>> list(sequencetools.yield_all_unordered_pairs_of_sequence([]))
        []

    Yields all unordered pairs of `sequence` with duplicate elements:

    ::

        >>> list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 1, 1]))
        [(1, 1), (1, 1), (1, 1)]

    Pairs are tuples instead of sets to accommodate duplicate `sequence`
    elements.

    Returns generator.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    sequence_copy = list(sequence)
    for i, x in enumerate(sequence_copy):
        for y in sequence_copy[i+1:]:
            pair = (x, y)
            yield pair
