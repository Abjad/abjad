def is_positive_integer_equivalent_number(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a positive integer-equivalent number. Otherwise false::

        >>> from abjad.tools import mathtools

    ::

        >>> mathtools.is_positive_integer_equivalent_number(Duration(4, 2))
        True

    Return boolean.
    '''
    from abjad.tools import mathtools

    return 0 < expr and mathtools.is_integer_equivalent_number(expr)
