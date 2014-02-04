# -*- encoding: utf-8 -*-
from __future__ import division
import copy
import math
from abjad.tools import mathtools


def repeat_sequence_to_length(sequence, length, start=0):
    '''Repeats `sequence` to nonnegative integer `length`.

    ::

        >>> sequencetools.repeat_sequence_to_length(range(5), 11)
        [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]

    Repeats `sequence` to nonnegative integer `length` from `start`:

    ::

        >>> sequencetools.repeat_sequence_to_length(range(5), 11, start=2)
        [2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2]

    Returns newly constructed `sequence` object.
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
