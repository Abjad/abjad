def partition_sequence_once_by_weights_exactly_with_overhang(sequence, weights):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``partition_sequence_by_weights_exactly()`` instead.

    Partition `sequence` elements once by `weights` exactly with overhang::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]

    ::

        >>> sequencetools.partition_sequence_once_by_weights_exactly_with_overhang(
        ...     sequence, [3, 9])
        [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]

    Return list sequence element reference lists.
    '''
    from abjad.tools import sequencetools

    return sequencetools.partition_sequence_by_weights_exactly(sequence, weights, cyclic=False, overhang=True)
