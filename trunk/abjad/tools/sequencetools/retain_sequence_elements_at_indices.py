# -*- encoding: utf-8 -*-


def retain_sequence_elements_at_indices(sequence, indices):
    '''Retain `sequence` elements at `indices`:

    ::

        >>> sequencetools.retain_sequence_elements_at_indices(range(20), [1, 16, 17, 18])
        [1, 16, 17, 18]

    Returns sequence elements in the order they appear in `sequence`.

    Ignore negative indices.

    Returns list.
    '''

    result = []

    for i, element in enumerate(sequence):
        if i in indices:
            result.append(element)

    return result
