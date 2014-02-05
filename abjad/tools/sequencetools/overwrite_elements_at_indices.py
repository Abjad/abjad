# -*- encoding: utf-8 -*-


def overwrite_elements_at_indices(sequence, pairs):
    '''Overwrites `sequence` elements at indices according to `pairs`.

    ::

        >>> sequencetools.overwrite_elements_at_indices(range(10), [(0, 3), (5, 3)])
        [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

    Set `pairs` to a list of ``(anchor_index, length)`` pairs.

    Returns new list.
    '''

    result = sequence[:]

    for anchor_index, length in pairs:
        anchor = result[anchor_index]
        start = anchor_index + 1
        stop = start + length - 1
        for i in range(start, stop):
            try:
                result[i] = anchor
            except IndexError:
                break

    return result
