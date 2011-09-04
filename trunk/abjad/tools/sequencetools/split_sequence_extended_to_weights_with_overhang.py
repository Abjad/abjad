from abjad.tools.sequencetools._split_sequence_extended_to_weights import _split_sequence_extended_to_weights


def split_sequence_extended_to_weights_with_overhang(sequence, weights):
    '''.. versionadded:: 2.0

    Split `sequence` extended to `weights` with overhang::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.split_sequence_extended_to_weights_with_overhang([1, 2, 3, 4, 5], [7, 7, 7])
        [[1, 2, 3, 1], [3, 4], [1, 1, 2, 3], [4, 5]]

    Return new object of `sequence` type.
    '''

    return _split_sequence_extended_to_weights(sequence, weights, overhang = True)
