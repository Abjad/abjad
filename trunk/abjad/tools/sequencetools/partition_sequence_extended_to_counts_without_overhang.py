def partition_sequence_extended_to_counts_without_overhang(sequence, counts):
    '''.. versionadded:: 2.0

    .. note:: Deprecated. Use ``partition_sequence_extended_to_counts()`` instead.

    Partition `sequence` extended to `counts` without overhang::

        >>> sequencetools.partition_sequence_extended_to_counts_without_overhang(
        ...     [1, 2, 3, 4], [6, 6, 6])
        [[1, 2, 3, 4, 1, 2], [3, 4, 1, 2, 3, 4], [1, 2, 3, 4, 1, 2]]

    Return new object of `sequence` type.
    '''
    from abjad.tools import sequencetools

    return sequencetools.partition_sequence_extended_to_counts(sequence, counts, overhang=False)
