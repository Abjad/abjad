def is_nonnegative_integer_equivalent_number(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a nonnegative integer-equivalent number. Otherwise false::

        >>> from abjad.tools import mathtools

    ::

        >>> mathtools.is_nonnegative_integer_equivalent_number(Duration(4, 2))
        True

    Return boolean.
    '''
    from abjad.tools import mathtools

    return mathtools.is_integer_equivalent_number(expr) and 0 <= expr
