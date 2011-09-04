from abjad.tools.sequencetools._split_sequence_by_weights import _split_sequence_by_weights


def split_sequence_cyclically_by_weights_without_overhang(sequence, weights):
    '''.. versionadded:: 2.0

    Split `sequence` cyclically by `weights` without overhang::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.split_sequence_cyclically_by_weights_without_overhang((10, -10, 10, -10), [3, 15, 3])
        [(3,), (7, -8), (-2, 1), (3,), (6, -9)]

    Return list of `sequence` objects.
    '''

    return _split_sequence_by_weights(sequence, weights, cyclic = True, overhang = False)
