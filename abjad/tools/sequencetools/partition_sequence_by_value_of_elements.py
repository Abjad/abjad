# -*- coding: utf-8 -*-
import collections
import itertools


def partition_sequence_by_value_of_elements(sequence):
    '''Groups `sequence` elements by value of elements.

    ::

        >>> sequence = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]

    ::

        >>> sequencetools.partition_sequence_by_value_of_elements(sequence)
        [(0, 0), (-1, -1), (2,), (3,), (-5,), (1, 1), (5,), (-5,)]

    Returns list of tuples of `sequence` element references.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must be sequence: {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    result = []
    g = itertools.groupby(sequence, lambda x: x)
    for n, group in g:
        result.append(tuple(group))


    return result
