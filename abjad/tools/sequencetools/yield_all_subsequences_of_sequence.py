# -*- coding: utf-8 -*-
import collections


def yield_all_subsequences_of_sequence(
    sequence,
    min_length=0,
    max_length=None,
    ):
    '''Yields all subsequences of `sequence`.

    Yields subsequences in lex order.

    ::

        >>> list(sequencetools.yield_all_subsequences_of_sequence([0, 1, 2]))
        [[], [0], [0, 1], [0, 1, 2], [1], [1, 2], [2]]

    Yields all subsequences of `sequence` greater than or equal to `min_length`
    in lex order:

    ::

        >>> list(sequencetools.yield_all_subsequences_of_sequence(
        ...     [0, 1, 2, 3, 4], min_length=3))
        [[0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4], [1, 2, 3], [1, 2, 3, 4], [2, 3, 4]]

    Yields all subsequences of `sequence` less than or equal to `max_length`
    in lex order:

    ::

        >>> for subsequence in sequencetools.yield_all_subsequences_of_sequence(
        ...     [0, 1, 2, 3, 4], max_length=3):
        ...     subsequence
        []
        [0]
        [0, 1]
        [0, 1, 2]
        [1]
        [1, 2]
        [1, 2, 3]
        [2]
        [2, 3]
        [2, 3, 4]
        [3]
        [3, 4]
        [4]

    Yields all subsequences of `sequence` greater than or equal to `min_length`
    and less than or equal to `max_length` in lex order:

    ::

        >>> list(sequencetools.yield_all_subsequences_of_sequence(
        ...     [0, 1, 2, 3, 4], min_length=3, max_length=3))
        [[0, 1, 2], [1, 2, 3], [2, 3, 4]]

    Returns generator.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    len_sequence = len(sequence)

    if max_length is None:
        max_length = len_sequence

    for i in range(len_sequence):
        start_j = min_length + i
        stop_j = min(max_length + i, len_sequence) + 1
        for j in range(start_j, stop_j):
            if i < j or i == 0:
                subsequence = sequence[i:j]
                yield subsequence
