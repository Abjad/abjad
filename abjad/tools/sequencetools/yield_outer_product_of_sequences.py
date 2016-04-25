# -*- coding: utf-8 -*-
import collections
import sys


def yield_outer_product_of_sequences(sequences):
    '''Yields outer product of `sequences`.

    ::

        >>> list(sequencetools.yield_outer_product_of_sequences(
        ...     [[1, 2, 3], ['a', 'b']]))
        [[1, 'a'], [1, 'b'], [2, 'a'], [2, 'b'], [3, 'a'], [3, 'b']]

    ::

        >>> list(sequencetools.yield_outer_product_of_sequences(
        ...     [[1, 2, 3], ['a', 'b'], ['X', 'Y']]))
        [[1, 'a', 'X'], [1, 'a', 'Y'], [1, 'b', 'X'], [1, 'b', 'Y'],
        [2, 'a', 'X'], [2, 'a', 'Y'], [2, 'b', 'X'], [2, 'b', 'Y'],
        [3, 'a', 'X'], [3, 'a', 'Y'], [3, 'b', 'X'], [3, 'b', 'Y']]

    ::

        >>> list(sequencetools.yield_outer_product_of_sequences(
        ...     [[1, 2, 3], [4, 5], [6, 7, 8]]))
        [[1, 4, 6], [1, 4, 7], [1, 4, 8], [1, 5, 6], [1, 5, 7], [1, 5, 8],
        [2, 4, 6], [2, 4, 7], [2, 4, 8], [2, 5, 6], [2, 5, 7], [2, 5, 8],
        [3, 4, 6], [3, 4, 7], [3, 4, 8], [3, 5, 6], [3, 5, 7], [3, 5, 8]]

    Returns generator.
    '''

    for sequence in sequences:
        if not isinstance(sequence, collections.Sequence):
            message = 'must by sequence {!r}.'
            message = message.format(sequence)
            raise Exception(message)

    def _helper(list1, list2):
        result = []
        for l1 in list1:
            for l2 in list2:
                result.extend([l1 + [l2]])
        return result

    sequences[0] = [[x] for x in sequences[0]]

    if sys.version_info[0] == 2:
        result = reduce(_helper, sequences)
    else:
        import functools
        result = functools.reduce(_helper, sequences)

    for element in result:
        yield element
