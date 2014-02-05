# -*- encoding: utf-8 -*-
import copy
from abjad.tools import mathtools


def repeat_sequence(sequence, n):
    '''Repeats `sequence` `n` times.

    ::

        >>> sequencetools.repeat_sequence((1, 2, 3, 4, 5), 3)
        (1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5)

    Repeats `sequence` ``0`` times:

    ::

        >>> sequencetools.repeat_sequence((1, 2, 3, 4, 5), 0)
        ()

    Returns newly constructed `sequence` object of copied `sequence` elements.
    '''

    if not mathtools.is_nonnegative_integer(n):
        message = 'must be nonnegative integer: {!r}.'
        message = message.format(n)
        raise ValueError(message)

    result = []
    for x in range(n):
        for element in sequence:
            result.append(copy.copy(element))
    return type(sequence)(result)
