def split_sequence_extended_to_weights_without_overhang(sequence, weights):
    '''.. versionadded:: 2.0

    Split `sequence` extended to `weights` without overhang::

        >>> sequencetools.split_sequence_extended_to_weights_without_overhang(
        ...     [1, 2, 3, 4, 5], [7, 7, 7])
        [[1, 2, 3, 1], [3, 4], [1, 1, 2, 3]]

    Return new object of `sequence` type.
    '''
    from abjad.tools import sequencetools

    return sequencetools.split_sequence_extended_to_weights(sequence, weights, overhang=False)
