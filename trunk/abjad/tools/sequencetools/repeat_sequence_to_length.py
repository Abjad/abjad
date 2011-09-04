from __future__ import division
from abjad.tools import mathtools
import copy
import math


def repeat_sequence_to_length(sequence, length, start = 0):
    '''.. versionadded:: 1.1

    Repeat `sequence` to nonnegative integer `length`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.repeat_sequence_to_length(range(5), 11)
        [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]

    Repeat `sequence` to nonnegative integer `length` from `start`::

        abjad> sequencetools.repeat_sequence_to_length(range(5), 11, start = 2)
        [2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2]

    Return newly constructed `sequence` object.

    .. versionchanged:: 2.0
        renamed ``listtools.repeat_list_to_length()`` to
        ``sequencetools.repeat_sequence_to_length()``.
    '''

    if not mathtools.is_nonnegative_integer(length):
        raise TypeError
    if len(sequence) <= 0:
        raise ValueError

    result = []
    start %= len(sequence)
    stop_index = start + length
    repetitions = int(math.ceil(stop_index / len(sequence)))
    for x in range(repetitions):
        for element in sequence:
            result.append(copy.copy(element))
    return type(sequence)(result[start:stop_index])
