from abjad.tools.sequencetools._partition_sequence_extended_to_counts import _partition_sequence_extended_to_counts


def partition_sequence_extended_to_counts_without_overhang(sequence, counts):
    '''.. versionadded:: 2.0

    Partition `sequence` extended to `counts` without overhang::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.partition_sequence_extended_to_counts_without_overhang([1, 2, 3, 4], [6, 6, 6])
        [[1, 2, 3, 4, 1, 2], [3, 4, 1, 2, 3, 4], [1, 2, 3, 4, 1, 2]]

    Return new object of `sequence` type.
    '''

    return _partition_sequence_extended_to_counts(sequence, counts, overhang = False)
