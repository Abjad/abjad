from abjad.tools import mathtools


def is_integer_equivalent_n_tuple(expr, n):
    r'''.. versionadded:: 2.9

    True when `expr` is a tuple of `n` integer-equivalent expressions::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.is_integer_equivalent_n_tuple((2.0, '3', Fraction(4, 1)), 3)
        True

    Otherwise false::

        >>> sequencetools.is_integer_equivalent_n_tuple((2.5, '3', Fraction(4, 1)), 3)
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == n and all([
        mathtools.is_integer_equivalent_expr(x) for x in expr])
