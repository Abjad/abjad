import numbers


def is_integer_equivalent_expr(expr):
    '''.. versionadded:: 2.5

    True when `expr` is an integer-equivalent number::


        >>> from abjad.tools import mathtools

    ::

        >>> mathtools.is_integer_equivalent_expr(12.0)
        True

    True when `expr` evaluates to an integer::

        >>> mathtools.is_integer_equivalent_expr('12')
        True

    Otherwise false::

        >>> mathtools.is_integer_equivalent_expr('foo')
        False

    Return boolean.
    '''
    from abjad.tools import mathtools

    if isinstance(expr, numbers.Number):
        return mathtools.is_integer_equivalent_number(expr)

    try:
        int(expr)
        return True
    except (TypeError, ValueError):
        return False
