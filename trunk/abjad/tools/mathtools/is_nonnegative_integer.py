import numbers


def is_nonnegative_integer(expr):
    '''.. versionadded:: 2.0

    True when `expr` equals a nonnegative integer::

        >>> from abjad.tools import mathtools

    ::

        >>> mathtools.is_nonnegative_integer(99)
        True

    ::

        >>> mathtools.is_nonnegative_integer(0)
        True

    Otherwise false::

        >>> mathtools.is_nonnegative_integer(-1)
        False

    Return boolean.
    '''

    if isinstance(expr, numbers.Number):
        if expr == int(expr):
            if 0 <= expr:
                return True

    return False
