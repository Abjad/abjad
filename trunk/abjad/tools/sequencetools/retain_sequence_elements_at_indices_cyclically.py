def retain_sequence_elements_at_indices_cyclically(sequence, indices, period, offset = 0):
    '''.. versionadded:: 2.0

    Retain `sequence` elements at `indices` mod `period` plus `offset`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.retain_sequence_elements_at_indices_cyclically(range(20), [0, 1], 5, 3)
        [3, 4, 8, 9, 13, 14, 18, 19]

    Ignore negative values in `indices`.

    Return list.
    '''

    result = []

    for i, element in enumerate(sequence):
        if (i - offset) % period in indices:
            result.append(element)

    return result
