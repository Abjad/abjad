def remove_sequence_elements_at_indices(sequence, indices):
    '''.. versionadded:: 2.0

    Remove `sequence` elements at `indices`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.remove_sequence_elements_at_indices(range(20), [1, 16, 17, 18])
        [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19]

    Ignore negative indices.

    Return list.
    '''

    result = []

    for i, element in enumerate(sequence):
        if i not in indices:
            #yield element
            result.append(element)

    return result
