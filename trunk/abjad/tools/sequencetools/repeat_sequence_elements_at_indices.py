def repeat_sequence_elements_at_indices(sequence, indices, total):
    '''.. versionadded:: 2.0

    Repeat `sequence` elements at `indices` to `total` length::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.repeat_sequence_elements_at_indices(range(10), [6, 7, 8], 3)
        [0, 1, 2, 3, 4, 5, [6, 6, 6], [7, 7, 7], [8, 8, 8], 9]

    Return list.
    '''

    result = []

    for i, element in enumerate(sequence):
        if i in indices:
            result.append(total * [element])
        else:
            result.append(element)

    return result
