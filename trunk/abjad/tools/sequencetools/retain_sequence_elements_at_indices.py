def retain_sequence_elements_at_indices(sequence, indices):
    '''.. versionadded:: 2.0

    Retain `sequence` elements at `indices`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.retain_sequence_elements_at_indices(range(20), [1, 16, 17, 18])
        [1, 16, 17, 18]

    Return sequence elements in the order they appear in `sequence`.

    Ignore negative indices.

    Return list.
    '''

    result = []

    for i, element in enumerate(sequence):
        if i in indices:
            result.append(element)

    return result
