# -*- encoding: utf-8 -*-


def repeat_sequence_elements_at_indices(sequence, indices, total):
    '''Repeat `sequence` elements at `indices` to `total` length:

    ::

        >>> sequencetools.repeat_sequence_elements_at_indices(range(10), [6, 7, 8], 3)
        [0, 1, 2, 3, 4, 5, [6, 6, 6], [7, 7, 7], [8, 8, 8], 9]

    Returns list.
    '''

    result = []

    for i, element in enumerate(sequence):
        if i in indices:
            result.append(total * [element])
        else:
            result.append(element)

    return result
