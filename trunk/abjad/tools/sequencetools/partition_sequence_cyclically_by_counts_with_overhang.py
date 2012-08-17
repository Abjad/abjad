def partition_sequence_cyclically_by_counts_with_overhang(sequence, counts):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``partition_sequence_by_counts()`` instead.

    Partition `sequence` cyclically by `counts` with overhang::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.partition_sequence_cyclically_by_counts_with_overhang(
        ...     range(16), [4, 6])
        [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13], [14, 15]]

    Return list of `sequence` objects.

    .. versionchanged:: 2.0
        renamed ``listtools.partition_sequence_cyclically_by_counts_with_overhang()`` to
        ``sequencetools.partition_sequence_cyclically_by_counts_with_overhang()``.
    '''
    from abjad.tools import sequencetools

    return sequencetools.partition_sequence_by_counts(sequence, counts, cyclic=True, overhang=True)
