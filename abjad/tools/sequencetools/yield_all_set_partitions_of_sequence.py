# -*- coding: utf-8 -*-
import collections


def yield_all_set_partitions_of_sequence(sequence):
    '''Yields all set partitions of `sequence`.

    ::

        >>> for set_partition in sequencetools.yield_all_set_partitions_of_sequence(
        ...     [21, 22, 23, 24]):
        ...     set_partition
        ...
        [[21, 22, 23, 24]]
        [[21, 22, 23], [24]]
        [[21, 22, 24], [23]]
        [[21, 22], [23, 24]]
        [[21, 22], [23], [24]]
        [[21, 23, 24], [22]]
        [[21, 23], [22, 24]]
        [[21, 23], [22], [24]]
        [[21, 24], [22, 23]]
        [[21], [22, 23, 24]]
        [[21], [22, 23], [24]]
        [[21, 24], [22], [23]]
        [[21], [22, 24], [23]]
        [[21], [22], [23, 24]]
        [[21], [22], [23], [24]]

    Returns set partitions in order of restricted growth function.

    Returns generator of list of lists.
    '''
    from abjad.tools import sequencetools

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    for rgf in sequencetools.yield_all_restricted_growth_functions_of_length(
        len(sequence)):
        partition = sequencetools.partition_sequence_by_restricted_growth_function(sequence, rgf)
        yield partition
