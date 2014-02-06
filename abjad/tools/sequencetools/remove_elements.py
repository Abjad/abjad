# -*- encoding: utf-8 -*-


def remove_elements(sequence, indices):
    '''Removes `sequence` elements at `indices`.

    ::

        >>> sequencetools.remove_elements(range(20), [1, 16, 17, 18])
        [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19]

    Ignores negative indices.

    Returns list.
    '''

    result = []

    for i, element in enumerate(sequence):
        if i not in indices:
            result.append(element)

    return result
