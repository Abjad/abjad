def partition_sequence_once_by_counts_without_overhang(sequence, counts):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``partition_sequence_by_counts()`` instead.

    Partition `sequence` once by `counts` without overhang::

        >>> sequencetools.partition_sequence_once_by_counts_without_overhang(range(16), [4, 6])
        [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9]]

    Return list of `sequence` objects.

    .. versionchanged:: 2.0
        renamed ``listtools.partition_sequence_once_by_counts_without_overhang()`` to
        ``sequencetools.partition_sequence_once_by_counts_without_overhang()``.
    '''
    from abjad.tools import sequencetools

    return sequencetools.partition_sequence_by_counts(sequence, counts, cyclic=False, overhang=False)
