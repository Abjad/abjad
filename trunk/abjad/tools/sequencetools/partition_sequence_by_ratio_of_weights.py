from abjad.tools import mathtools
from abjad.tools.mathtools.cumulative_sums import cumulative_sums
from abjad.tools.mathtools.weight import weight
from abjad.tools.sequencetools.flatten_sequence import flatten_sequence
from fractions import Fraction


def partition_sequence_by_ratio_of_weights(sequence, weights):
    '''.. versionadded:: 2.0

    Partition `sequence` by ratio of `weights`::

        abjad> from abjad.tools import sequencetools

    ::


        abjad> sequencetools.partition_sequence_by_ratio_of_weights([1] * 10, [1, 1, 1])
        [[1, 1, 1], [1, 1, 1, 1], [1, 1, 1]]

    ::

        abjad> sequencetools.partition_sequence_by_ratio_of_weights([1] * 10, [1, 1, 1, 1])
        [[1, 1, 1], [1, 1], [1, 1, 1], [1, 1]]

    ::

        abjad> sequencetools.partition_sequence_by_ratio_of_weights([1] * 10, [2, 2, 3])
        [[1, 1, 1], [1, 1, 1], [1, 1, 1, 1]]

    ::

        abjad> sequencetools.partition_sequence_by_ratio_of_weights([1] * 10, [3, 2, 2])
        [[1, 1, 1, 1], [1, 1, 1], [1, 1, 1]]

    ::

        abjad> sequencetools.partition_sequence_by_ratio_of_weights([1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2], [1, 1])
        [[1, 1, 1, 1, 1, 1, 2, 2], [2, 2, 2, 2]]

    ::

        abjad> sequencetools.partition_sequence_by_ratio_of_weights([1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2], [1, 1, 1])
        [[1, 1, 1, 1, 1, 1], [2, 2, 2], [2, 2, 2]]


    Weights of parts of returned list equal `weights_ratio` proportions
    with some rounding magic.

    Return list of lists.
    '''

    list_weight = weight(sequence)
    weights_parts = mathtools.partition_integer_by_ratio(list_weight, weights)
    cumulative_weights = cumulative_sums(weights_parts)

    result = []
    sublist = []
    result.append(sublist)
    cur_cumulative_weight = cumulative_weights.pop(0)
    for n in sequence:
        if not isinstance(n, (int, long, float, Fraction)):
            raise TypeError('must be number.')
        sublist.append(n)
        while cur_cumulative_weight <= weight(flatten_sequence(result)):
            try:
                cur_cumulative_weight = cumulative_weights.pop(0)
                sublist = []
                result.append(sublist)
            except IndexError:
                break

    return result
