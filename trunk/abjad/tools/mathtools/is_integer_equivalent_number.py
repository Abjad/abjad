import numbers


def is_integer_equivalent_number(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a number and `expr` is equivalent to an integer::

        >>> from abjad.tools import mathtools

    ::

        >>> mathtools.is_integer_equivalent_number(12.0)
        True

    Otherwise false::

        >>> mathtools.is_integer_equivalent_number(Duration(1, 2))
        False

    Return boolean.
    '''

    if isinstance(expr, numbers.Number):
        if int(expr) == expr:
            return True

    return False
