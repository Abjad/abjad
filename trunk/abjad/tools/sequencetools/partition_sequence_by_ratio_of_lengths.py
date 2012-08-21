from abjad.tools import mathtools


def partition_sequence_by_ratio_of_lengths(sequence, lengths):
    '''.. versionadded:: 2.0

    Partition `sequence` by ratio of `lengths`::

        >>> sequence = tuple(range(10))

    ::

        >>> sequencetools.partition_sequence_by_ratio_of_lengths(sequence, [1, 1, 2])
        [(0, 1, 2), (3, 4), (5, 6, 7, 8, 9)]

    Use rounding magic to avoid fractional part lengths.

    Return list of `sequence` objects.
    '''
    from abjad.tools import sequencetools

    lengths = mathtools.partition_integer_by_ratio(len(sequence), lengths)
    return sequencetools.partition_sequence_by_counts(sequence, lengths, cyclic=False, overhang=False)
