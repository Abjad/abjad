from numbers import Number


def is_nonnegative_integer(expr):
    '''.. versionadded:: 2.0

    True when `expr` equals a nonnegative integer::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.is_nonnegative_integer(99)
        True

    ::

        abjad> mathtools.is_nonnegative_integer(0)
        True

    Otherwise false::

        abjad> mathtools.is_nonnegative_integer(-1)
        False

    Return boolean.
    '''

    if isinstance(expr, Number):
        if expr == int(expr):
            if 0 <= expr:
                return True

    return False
