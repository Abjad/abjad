from abjad.tools.sequencetools._partition_sequence_by_counts import _partition_sequence_by_counts


def partition_sequence_cyclically_by_counts_with_overhang(sequence, counts):
    '''.. versionadded:: 1.1

    Partition `sequence` cyclically by `counts` with overhang::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.partition_sequence_cyclically_by_counts_with_overhang(range(16), [4, 6])
        [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13], [14, 15]]

    Return list of `sequence` objects.

    .. versionchanged:: 2.0
        renamed ``listtools.partition_sequence_cyclically_by_counts_with_overhang()`` to
        ``sequencetools.partition_sequence_cyclically_by_counts_with_overhang()``.
    '''

    return _partition_sequence_by_counts(sequence, counts, cyclic = True, overhang = True)
