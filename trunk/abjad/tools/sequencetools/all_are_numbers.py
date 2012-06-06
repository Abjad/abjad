import numbers


def all_are_numbers(expr):
    '''.. versionadded:: 1.1

    True when `expr` is a sequence and all elements in `expr` are numbers::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.all_are_numbers([1, 2, 3.0, Fraction(13, 8)])
        True

    True when `expr` is an empty sequence::

        >>> sequencetools.all_are_numbers([])
        True

    False otherwise::

        >>> sequencetools.all_are_numbers(17)
        False

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``sequencetools.is_numeric()`` to
        ``sequencetools.all_are_numbers()``.
    '''

    try:
        return all([isinstance(x, numbers.Number) for x in expr])
    except TypeError:
        return False
