from abjad.tools.sequencetools.is_restricted_growth_function import is_restricted_growth_function


def partition_sequence_by_restricted_growth_function(sequence, restricted_growth_function):
    '''.. versionadded:: 2.0

    Partition `sequence` by `restricted_growth_function`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> l = range(10)
        abjad> rgf = [1, 1, 2, 2, 1, 2, 3, 3, 2, 4]
        abjad> sequencetools.partition_sequence_by_restricted_growth_function(l, rgf)
        [[0, 1, 4], [2, 3, 5, 8], [6, 7], [9]]

    Raise value error when `sequence` length does not equal `restricted_growth_function` length.

    Return list of lists.
    '''

    if not is_restricted_growth_function(restricted_growth_function):
        raise ValueError('must be restricted growth function.')

    if not len(sequence) == len(restricted_growth_function):
        raise ValueError('lengths must be equal.')

    partition = []
    for part_index in range(max(restricted_growth_function)):
        part = []
        partition.append(part)

    for n, part_number in zip(sequence, restricted_growth_function):
        part_index = part_number - 1
        part = partition[part_index]
        part.append(n)

    return partition
