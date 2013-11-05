# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
import copy


# TODO: generalize count from a single integer count to a list to read cyclically #
def repeat_sequence_elements_n_times_each(sequence, n):
    '''Repeat `sequence` elements `n` times each:

    ::

        >>> sequencetools.repeat_sequence_elements_n_times_each((1, -1, 2, -3, 5, -5, 6), 2)
        (1, 1, -1, -1, 2, 2, -3, -3, 5, 5, -5, -5, 6, 6)

    Returns newly constructed `sequence` object with copied `sequence` elements.
    '''

    if not mathtools.is_nonnegative_integer(n):
        raise ValueError

    result = []
    for element in sequence:
        for x in range(n):
            result.append(copy.copy(element))
    return type(sequence)(result)
