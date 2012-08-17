def yield_all_set_partitions_of_sequence(sequence):
    '''.. versionadded:: 2.0

    Yield all set partitions of `sequence` in restricted growth function order::

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

    Return generator of list of lists.
    '''
    from abjad.tools import sequencetools

    for rgf in sequencetools.yield_all_restricted_growth_functions_of_length(len(sequence)):
        partition = sequencetools.partition_sequence_by_restricted_growth_function(sequence, rgf)
        yield partition
