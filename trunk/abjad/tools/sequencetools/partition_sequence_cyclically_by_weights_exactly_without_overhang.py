def partition_sequence_cyclically_by_weights_exactly_without_overhang(sequence, weights):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``partition_sequence_by_weights_exactly()`` instead.

    Partition `sequence` elements cyclically by `weights` exactly without overhang::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]

    ::

        >>> sequencetools.partition_sequence_cyclically_by_weights_exactly_without_overhang(
        ...     sequence, [12])
        [[3, 3, 3, 3], [4, 4, 4]]

    Return list of sequence element reference lists.
    '''
    from abjad.tools import sequencetools

    return sequencetools.partition_sequence_by_weights_exactly(sequence, weights, cyclic=True, overhang=False)
