from abjad.tools import mathtools


def is_integer_equivalent_pair(expr):
    r'''.. versionadded:: 2.9

    True when `expr` is a pair of integer-equivalent expressions::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.is_integer_equivalent_pair((2.0, '3'))
        True

    Otherwise false::

        >>> sequencetools.is_integer_equivalent_pair((2.5, '3'))
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 2 and all([
        mathtools.is_integer_equivalent_expr(x) for x in expr])
