def partition_sequence_cyclically_by_weights_at_least_with_overhang(sequence, weights):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``partition_sequence_by_weights_at_least()`` instead.

    Partition `sequence` elements cyclically by `weights` at least with overhang::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]

    ::

        >>> sequencetools.partition_sequence_cyclically_by_weights_at_least_with_overhang(
        ...     sequence, [10, 4])
        [[3, 3, 3, 3], [4], [4, 4, 4], [5], [5]]

    Return list sequence element reference lists.
    '''
    from abjad.tools import sequencetools

    return sequencetools.partition_sequence_by_weights_at_least(sequence, weights, cyclic=True, overhang=True)
