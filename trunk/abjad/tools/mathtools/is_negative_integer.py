from numbers import Number


def is_negative_integer(expr):
    '''.. versionadded:: 2.0

    True when `expr` equals a negative integer::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.is_negative_integer(-1)
        True

    Otherwise false::

        abjad> mathtools.is_negative_integer(0)
        False

    ::

        abjad> mathtools.is_negative_integer(99)
        False

    Return boolean.
    '''

    if isinstance(expr, Number):
        if expr == int(expr):
            if expr < 0:
                return True

    return False
