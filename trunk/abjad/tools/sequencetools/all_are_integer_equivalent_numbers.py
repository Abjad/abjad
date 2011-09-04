from abjad.tools import mathtools


def all_are_integer_equivalent_numbers(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a sequence and all elements in `expr` are integer-equivalent numbers::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.all_are_integer_equivalent_numbers([1, 2, 3.0, Fraction(4, 1)])
        True

    Otherwise false::

        abjad> sequencetools.all_are_integer_equivalent_numbers([1, 2, 3.5, 4])
        False

    Return boolean.
    '''

    try:
        return all([mathtools.is_integer_equivalent_number(x) for x in expr])
    except TypeError:
        return False
