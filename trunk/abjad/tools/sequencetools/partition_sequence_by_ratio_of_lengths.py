from abjad.tools import mathtools
from abjad.tools.sequencetools.partition_sequence_once_by_counts_without_overhang import partition_sequence_once_by_counts_without_overhang


def partition_sequence_by_ratio_of_lengths(sequence, lengths):
    '''.. versionadded:: 2.0

    Partition `sequence` by ratio of `lengths`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.partition_sequence_by_ratio_of_lengths(tuple(range(10)), [1, 1, 2])
        [(0, 1, 2), (3, 4), (5, 6, 7, 8, 9)]

    Use rounding magic to avoid fractional part lengths.

    Return list of `sequence` objects.
    '''

    lengths = mathtools.partition_integer_by_ratio(len(sequence), lengths)
    return partition_sequence_once_by_counts_without_overhang(sequence, lengths)
