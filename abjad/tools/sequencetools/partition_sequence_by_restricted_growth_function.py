# -*- coding: utf-8 -*-


def partition_sequence_by_restricted_growth_function(
    sequence,
    restricted_growth_function,
    ):
    '''Partitions `sequence` by `restricted_growth_function`.

    ::

        >>> l = range(10)
        >>> rgf = [1, 1, 2, 2, 1, 2, 3, 3, 2, 4]

    ::

        >>> sequencetools.partition_sequence_by_restricted_growth_function(
        ...     l, rgf)
        [[0, 1, 4], [2, 3, 5, 8], [6, 7], [9]]

    Raises value error when `sequence` length does not equal
    `restricted_growth_function` length.

    Returns list of lists.
    '''
    from abjad.tools import sequencetools

    restricted_growth_function = sequencetools.Sequence(
        restricted_growth_function)
    if not restricted_growth_function.is_restricted_growth_function():
        message = 'must be restricted growth function: {!r}.'
        message = message.format(restricted_growth_function)
        raise ValueError(message)

    if not len(sequence) == len(restricted_growth_function):
        message = 'lengths must be equal.'
        raise ValueError(message)

    partition = []
    for part_index in range(max(restricted_growth_function)):
        part = []
        partition.append(part)

    for n, part_number in zip(sequence, restricted_growth_function):
        part_index = part_number - 1
        part = partition[part_index]
        part.append(n)

    return partition
