from abjad.tools.mathtools.is_integer_equivalent_number import is_integer_equivalent_number


def is_nonnegative_integer_equivalent_number(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a nonnegative integer-equivalent number. Otherwise false::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.is_nonnegative_integer_equivalent_number(Duration(4, 2))
        True

    Return boolean.
    '''

    return is_integer_equivalent_number(expr) and 0 <= expr
