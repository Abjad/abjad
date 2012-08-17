import fractions
from abjad.tools import mathtools


def partition_sequence_by_ratio_of_weights(sequence, weights):
    '''.. versionadded:: 2.0

    Partition `sequence` by ratio of `weights`::

        >>> sequencetools.partition_sequence_by_ratio_of_weights([1] * 10, [1, 1, 1])
        [[1, 1, 1], [1, 1, 1, 1], [1, 1, 1]]

    ::

        >>> sequencetools.partition_sequence_by_ratio_of_weights([1] * 10, [1, 1, 1, 1])
        [[1, 1, 1], [1, 1], [1, 1, 1], [1, 1]]

    ::

        >>> sequencetools.partition_sequence_by_ratio_of_weights([1] * 10, [2, 2, 3])
        [[1, 1, 1], [1, 1, 1], [1, 1, 1, 1]]

    ::

        >>> sequencetools.partition_sequence_by_ratio_of_weights([1] * 10, [3, 2, 2])
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

    Return list of lists.
    '''
    from abjad.tools import sequencetools

    list_weight = mathtools.weight(sequence)
    weights_parts = mathtools.partition_integer_by_ratio(list_weight, weights)
    cumulative_weights = mathtools.cumulative_sums(weights_parts)

    result = []
    sublist = []
    result.append(sublist)
    cur_cumulative_weight = cumulative_weights.pop(0)
    for n in sequence:
        if not isinstance(n, (int, long, float, fractions.Fraction)):
            raise TypeError('must be number.')
        sublist.append(n)
        while cur_cumulative_weight <= mathtools.weight(sequencetools.flatten_sequence(result)):
            try:
                cur_cumulative_weight = cumulative_weights.pop(0)
                sublist = []
                result.append(sublist)
            except IndexError:
                break

    return result
