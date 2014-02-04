# -*- encoding: utf-8 -*-


def remove_sequence_elements_at_indices_cyclically(
    sequence, 
    indices, 
    period, 
    offset=0,
    ):
    '''Removes `sequence` elements at `indices` mod `period` plus `offset`.

    ::

        >>> sequencetools.remove_sequence_elements_at_indices_cyclically(range(20), [0, 1], 5, 3)
        [0, 1, 2, 5, 6, 7, 10, 11, 12, 15, 16, 17]

    Ignores negative indices.

    Returns list.
    '''

    result = []

    for i, element in enumerate(sequence):
        if (i - offset) % period not in indices:
            result.append(element)

    return result
