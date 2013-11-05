# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def divide_sequence_elements_by_greatest_common_divisor(sequence):
    '''Divide `sequence` elements by greatest common divisor:

    ::

        >>> sequencetools.divide_sequence_elements_by_greatest_common_divisor([2, 2, -8, -16])
        [1, 1, -4, -8]

    Allow negative `sequence` elements.

    Raise type error on noninteger `sequence` elements.

    Raise not implemented error when ``0`` in `sequence`.

    Returns new `sequence` object.
    '''

    gcd = mathtools.greatest_common_divisor(*sequence)
    result = [element / gcd for element in sequence]
    return type(sequence)(result)
