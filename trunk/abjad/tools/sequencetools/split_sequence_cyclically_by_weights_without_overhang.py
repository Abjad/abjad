def split_sequence_cyclically_by_weights_without_overhang(sequence, weights):
    '''.. versionadded:: 2.0

    .. note:: Deprecated. Use ``split_sequence_by_weights()`` instead.

    Split `sequence` cyclically by `weights` without overhang::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.split_sequence_cyclically_by_weights_without_overhang(
        ...         (10, -10, 10, -10), [3, 15, 3])
        [(3,), (7, -8), (-2, 1), (3,), (6, -9)]

    Return list of `sequence` objects.
    '''
    from abjad.tools import sequencetools

    return sequencetools.split_sequence_by_weights(sequence, weights, cyclic=True, overhang=False)
