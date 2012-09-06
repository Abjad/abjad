import numbers


def is_positive_integer(expr):
    '''.. versionadded:: 2.0

    True when `expr` equals a positive integer::

        >>> from abjad.tools import mathtools

    ::

        >>> mathtools.is_positive_integer(99)
        True

    Otherwise false::

        >>> mathtools.is_positive_integer(0)
        False

    ::

        >>> mathtools.is_positive_integer(-1)
        False

    Return boolean.
    '''

    if isinstance(expr, numbers.Number):
        if expr == int(expr):
            if 0 < expr:
                return True

    return False
