from abjad.tools import mathtools


def all_are_positive_integer_equivalent_numbers(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a sequence and all elements in `expr` are positive
    integer-equivalent numbers. Otherwise false::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.all_are_positive_integer_equivalent_numbers([Fraction(4, 2), 2.0, 2])
        True

    Return boolean.
    '''

    try:
        return all([mathtools.is_positive_integer_equivalent_number(x) for x in expr])
    except TypeError:
        return False
