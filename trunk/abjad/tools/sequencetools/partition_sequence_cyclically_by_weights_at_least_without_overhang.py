def partition_sequence_cyclically_by_weights_at_least_without_overhang(sequence, weights):
    '''.. versionadded:: 1.1

    Partition `sequence` elements cyclically by `weights` at least without overhang::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
        >>> sequencetools.partition_sequence_cyclically_by_weights_at_least_without_overhang(
        ...     sequence, [10, 4])
        [[3, 3, 3, 3], [4], [4, 4, 4], [5]]

    Return list sequence element reference lists.
    '''
    from abjad.tools.sequencetools._partition_sequence_elements_by_weights_at_least import \
        _partition_sequence_elements_by_weights_at_least

    return _partition_sequence_elements_by_weights_at_least(
        sequence, weights, cyclic=True, overhang=False)
