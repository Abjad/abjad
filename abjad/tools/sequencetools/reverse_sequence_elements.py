# -*- encoding: utf-8 -*-
from abjad.tools.sequencetools.reverse_sequence import reverse_sequence


def reverse_sequence_elements(sequence):
    '''Reverse `sequence` elements:

    ::

        >>> sequencetools.reverse_sequence_elements([1, (2, 3, 4), 5, (6, 7)])
        [1, (4, 3, 2), 5, (7, 6)]

    Returns new `sequence` object.
    '''

    result = []
    for element in sequence:
        try:
            result.append(reverse_sequence(element))
        except TypeError:
            result.append(element)
    result = type(sequence)(result)
    return result
