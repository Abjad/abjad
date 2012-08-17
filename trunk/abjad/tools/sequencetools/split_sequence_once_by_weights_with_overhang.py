def split_sequence_once_by_weights_with_overhang(sequence, weights):
    '''.. versionadded:: 2.0

    Split `sequence` once by `weights` with overhang::

        >>> sequencetools.split_sequence_once_by_weights_with_overhang(
        ...     (10, -10, 10, -10), [3, 15, 3])
        [(3,), (7, -8), (-2, 1), (9, -10)]

    Return list of `sequence` objects.
    '''
    from abjad.tools import sequencetools

    return sequencetools.split_sequence_by_weights(sequence, weights, cyclic=False, overhang=True)
