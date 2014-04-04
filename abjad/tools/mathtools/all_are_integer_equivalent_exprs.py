# -*- encoding: utf-8 -*-


def all_are_integer_equivalent_exprs(expr):
    '''Is true when `expr` is a sequence and all elements in `expr` are
    integer-equivalent expressions.

    ::

        >>> mathtools.all_are_integer_equivalent_exprs([1, '2', 3.0, Fraction(4, 1)])
        True

    Otherwise false:

    ::

        >>> mathtools.all_are_integer_equivalent_exprs([1, '2', 3.5, 4])
        False

    Returns boolean.
    '''
    from abjad.tools import mathtools

    try:
        return all(mathtools.is_integer_equivalent_expr(x) for x in expr)
    except TypeError:
        return False