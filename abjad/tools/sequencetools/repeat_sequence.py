# -*- coding: utf-8 -*-
import collections
from abjad.tools import mathtools


def repeat_sequence(sequence, n):
    '''Repeats `sequence` `n` times.

    ..  container:: example

        **Example 1.** Repeats tuple three times:

        ::

            >>> sequencetools.repeat_sequence((1, 2, 3, 4, 5), 3)
            (1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5)

    ..  container:: example

        **Example 2.** Repeats tuple zero times:

        ::

            >>> sequencetools.repeat_sequence((1, 2, 3, 4, 5), 0)
            ()

    ..  container:: example

        **Example 3.** Repeats list three times:

        ::

            >>> sequencetools.repeat_sequence([1, 2, 3, 4, 5], 3)
            [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]

    Repeats references to `sequence` elements; does not copy `sequence`
    elements.

    Returns new object of `sequence` type.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    if not mathtools.is_nonnegative_integer(n):
        message = 'must be nonnegative integer: {!r}.'
        message = message.format(n)
        raise ValueError(message)

    result = []
    for x in range(n):
        for element in sequence:
            result.append(element)

    result = sequence_type(result)
    return result
