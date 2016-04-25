# -*- coding: utf-8 -*-


def overwrite_elements(sequence, pairs):
    '''Overwrites `sequence` elements at indices according to `pairs`.

    ..  container:: example

        **Example 1.** Overwrites range elements:

        ::

            >>> pairs = [(0, 3), (5, 3)]
            >>> sequencetools.overwrite_elements(range(10), pairs)
            [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

        Returns list.

    ..  container:: example

        **Example 2.** Overwrites list elements:

        ::

            >>> pairs = [(0, 3), (5, 3)]
            >>> sequencetools.overwrite_elements(list(range(10)), pairs)
            [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

        Returns new list.

    ..  container:: example

        **Example 3.** Overwrites tuple elements:

        ::

            >>> pairs = [(0, 3), (5, 3)]
            >>> sequencetools.overwrite_elements(tuple(range(10)), pairs)
            [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

        Returns list.

    Set `pairs` to a list of ``(anchor_index, length)`` pairs.

    Coerces input to list.

    Returns new list.
    '''
    sequence = list(sequence)
    result = list(sequence)
    for anchor_index, length in pairs:
        anchor = result[anchor_index]
        start = anchor_index + 1
        stop = start + length - 1
        for i in range(start, stop):
            try:
                result[i] = anchor
            except IndexError:
                break
    assert isinstance(result, list), repr(result)
    return result
