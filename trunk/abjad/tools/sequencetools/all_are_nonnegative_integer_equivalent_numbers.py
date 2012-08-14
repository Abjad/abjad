from abjad.tools import mathtools


def all_are_nonnegative_integer_equivalent_numbers(expr):
    '''.. versionadded:: 2.0

    True `expr` is a sequence and when all elements in `expr` are nonnegative
    integer-equivalent numbers. Otherwise false::

        >>> from abjad.tools import sequencetools

    ::


        >>> expr = [0, 0.0, Fraction(0), 2, 2.0, Fraction(2)]
        >>> sequencetools.all_are_nonnegative_integer_equivalent_numbers(expr)
        True

    Return boolean.
    '''

    try:
        return all([mathtools.is_nonnegative_integer_equivalent_number(x) for x in expr])
    except TypeError:
        return False
