from abjad.tools.sequencetools.partition_sequence_by_restricted_growth_function import partition_sequence_by_restricted_growth_function
from abjad.tools.sequencetools.yield_all_restricted_growth_functions_of_length import yield_all_restricted_growth_functions_of_length


def yield_all_set_partitions_of_sequence(sequence):
    '''.. versionadded:: 2.0

    Yield all set partitions of `sequence` in restricted growth function order::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> for set_partition in sequencetools.yield_all_set_partitions_of_sequence([21, 22, 23, 24]):
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

    for rgf in yield_all_restricted_growth_functions_of_length(len(sequence)):
        partition = partition_sequence_by_restricted_growth_function(sequence, rgf)
        yield partition
