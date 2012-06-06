from abjad.tools.mathtools.is_integer_equivalent_number import is_integer_equivalent_number


def is_positive_integer_equivalent_number(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a positive integer-equivalent number. Otherwise false::

        >>> from abjad.tools import mathtools

    ::

        >>> mathtools.is_positive_integer_equivalent_number(Duration(4, 2))
        True

    Return boolean.
    '''

    return 0 < expr and is_integer_equivalent_number(expr)
