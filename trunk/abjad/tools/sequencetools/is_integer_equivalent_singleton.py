from abjad.tools import mathtools


def is_integer_equivalent_singleton(expr):
    r'''.. versionadded:: 2.9

    True when `expr` is a singleton of integer-equivalent expressions::
        
        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.is_integer_equivalent_singleton((2.0,))
        True

    Otherwise false::

        >>> sequencetools.is_integer_equivalent_singleton((2.5,))
        False

    Return boolean.
    '''

    return isinstance(expr, tuple) and len(expr) == 1 and all([
        mathtools.is_integer_equivalent_expr(x) for x in expr])
