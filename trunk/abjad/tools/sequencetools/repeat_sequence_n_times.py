from abjad.tools import mathtools
import copy


def repeat_sequence_n_times(sequence, n):
    '''.. versionadded:: 2.0

    Repeat `sequence` `n` times::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.repeat_sequence_n_times((1, 2, 3, 4, 5), 3)
        (1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5)

    Repeat `sequence` ``0`` times::

        abjad> sequencetools.repeat_sequence_n_times((1, 2, 3, 4, 5), 0)
        ()

    Return newly constructed `sequence` object of copied `sequence` elements.
    '''

    if not mathtools.is_nonnegative_integer(n):
        raise ValueError('must be nonnegative integer.')

    result = []
    for x in range(n):
        for element in sequence:
            result.append(copy.copy(element))
    return type(sequence)(result)
