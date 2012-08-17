def partition_sequence_once_by_weights_at_most_without_overhang(sequence, weights):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``partition_sequence_by_weights_at_most()`` instead.

    Partition `sequence` elements once by `weights` at most without overhang::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]

    ::

        >>> sequencetools.partition_sequence_once_by_weights_at_most_without_overhang(
        ...     sequence, [10, 4])
        [[3, 3, 3], [3]]

    Return list sequence element reference lists.
    '''
    from abjad.tools import sequencetools

    return sequencetools.partition_sequence_by_weights_at_most(sequence, weights, cyclic=False, overhang=False)
