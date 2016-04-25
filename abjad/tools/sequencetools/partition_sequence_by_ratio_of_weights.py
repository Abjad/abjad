# -*- coding: utf-8 -*-
import collections
import fractions
from abjad.tools import mathtools


def partition_sequence_by_ratio_of_weights(sequence, weights):
    '''Partitions `sequence` by ratio of `weights`.

    ::

        >>> sequencetools.partition_sequence_by_ratio_of_weights(
        ...     [1] * 10, [1, 1, 1])
        [[1, 1, 1], [1, 1, 1, 1], [1, 1, 1]]

    ::

        >>> sequencetools.partition_sequence_by_ratio_of_weights(
        ...     [1] * 10, [1, 1, 1, 1])
        [[1, 1, 1], [1, 1], [1, 1, 1], [1, 1]]

    ::

        >>> sequencetools.partition_sequence_by_ratio_of_weights(
        ...     [1] * 10, [2, 2, 3])
        [[1, 1, 1], [1, 1, 1], [1, 1, 1, 1]]

    ::

        >>> sequencetools.partition_sequence_by_ratio_of_weights(
        ...     [1] * 10, [3, 2, 2])
        [[1, 1, 1, 1], [1, 1, 1], [1, 1, 1]]

    ::

        >>> sequencetools.partition_sequence_by_ratio_of_weights(
        ...     [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2], [1, 1])
        [[1, 1, 1, 1, 1, 1, 2, 2], [2, 2, 2, 2]]

    ::

        >>> sequencetools.partition_sequence_by_ratio_of_weights(
        ...     [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2], [1, 1, 1])
        [[1, 1, 1, 1, 1, 1], [2, 2, 2], [2, 2, 2]]


    Weights of parts of returned list equal `weights_ratio` proportions
    with some rounding magic.

    Returns list of lists.
    '''
    from abjad.tools import sequencetools

    if not isinstance(sequence, collections.Sequence):
        message = 'must be sequence: {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    list_weight = mathtools.weight(sequence)
    weights_parts = mathtools.partition_integer_by_ratio(list_weight, weights)
    cumulative_weights = mathtools.cumulative_sums(weights_parts, start=None)

    result = []
    sublist = []
    result.append(sublist)
    current_cumulative_weight = cumulative_weights.pop(0)
    for n in sequence:
        if not isinstance(n, (int, float, fractions.Fraction)):
            message = 'must be number: {!r}.'
            message = message.format(n)
            raise TypeError(message)
        sublist.append(n)
        while current_cumulative_weight <= \
            mathtools.weight(sequencetools.flatten_sequence(result)):
            try:
                current_cumulative_weight = cumulative_weights.pop(0)
                sublist = []
                result.append(sublist)
            except IndexError:
                break

    return result
