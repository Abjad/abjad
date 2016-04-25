# -*- coding: utf-8 -*-
import collections
import math
from abjad.tools import mathtools


def repeat_sequence_to_length(sequence, length, start=0):
    '''Repeats `sequence` to nonnegative integer `length`.

    ..  container:: example

        **Example 1.** Repeats list to length 11:

        ::

            >>> sequencetools.repeat_sequence_to_length(list(range(5)), 11)
            [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]

    ..  container:: example

        **Example 2.** Repeats `sequence` to nonnegative integer `length` from
        `start`:

        ::

            >>> sequencetools.repeat_sequence_to_length(
            ...     list(range(5)), 11, start=2)
            [2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2]

        **Example 3.** Repeats tuple to length 11:

        ::

            >>> sequencetools.repeat_sequence_to_length(tuple(range(5)), 11)
            (0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0)

    Copies `sequence` element references; does not copy `sequence` elements.

    Returns new object of `sequence` type.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    if not mathtools.is_nonnegative_integer(length):
        raise TypeError
    if len(sequence) <= 0:
        raise ValueError

    result = []
    start %= len(sequence)
    stop_index = start + length
    repetitions = int(math.ceil(float(stop_index) / len(sequence)))
    for x in range(repetitions):
        for element in sequence:
            result.append(element)

    return sequence_type(result[start:stop_index])
