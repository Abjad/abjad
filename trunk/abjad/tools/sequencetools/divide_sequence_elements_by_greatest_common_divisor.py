from abjad.tools import mathtools


def divide_sequence_elements_by_greatest_common_divisor(sequence):
    '''.. versionadded:: 2.0

    Divide `sequence` elements by greatest common divisor::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.divide_sequence_elements_by_greatest_common_divisor([2, 2, -8, -16])
        [1, 1, -4, -8]

    Allow negative `sequence` elements.

    Raise type error on noninteger `sequence` elements.

    Raise not implemented error when ``0`` in `sequence`.

    Return new `sequence` object.
    '''

    gcd = mathtools.greatest_common_divisor(*sequence)
    result = [element / gcd for element in sequence]
    return type(sequence)(result)
