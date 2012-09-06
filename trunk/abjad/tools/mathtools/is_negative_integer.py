import numbers


def is_negative_integer(expr):
    '''.. versionadded:: 2.0

    True when `expr` equals a negative integer::

        >>> from abjad.tools import mathtools

    ::

        >>> mathtools.is_negative_integer(-1)
        True

    Otherwise false::

        >>> mathtools.is_negative_integer(0)
        False

    ::

        >>> mathtools.is_negative_integer(99)
        False

    Return boolean.
    '''

    if isinstance(expr, numbers.Number):
        if expr == int(expr):
            if expr < 0:
                return True

    return False
