# -*- coding: utf-8 -*-
import collections


def overwrite_elements(sequence, pairs):
    '''Overwrites `sequence` elements at indices according to `pairs`.

    ..  container:: example

        Sequence for examples:

        ::

            >>> sequence = list(range(10))

    ..  container:: example

        **Example 1.** Overwrites list of first ten integers with a run of 0s
        and a run of 5s:

        ::

            >>> pairs = [(0, 3), (5, 3)]
            >>> sequencetools.overwrite_elements(sequence, pairs)
            [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

    ..  container:: example

        **Example 2.** Overwrites tuples of first ten integers with a run of 0s
        and a run of 5s:

        ::

            >>> pairs = [(0, 3), (5, 3)]
            >>> sequencetools.overwrite_elements(tuple(sequence), pairs)
            (0, 0, 0, 3, 4, 5, 5, 5, 8, 9)

    Set `pairs` to a list of ``(anchor_index, length)`` pairs.

    Returns new list.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must be sequence: {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

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

    result = sequence_type(result)

    return result