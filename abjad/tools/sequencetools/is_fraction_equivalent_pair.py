# -*- encoding: utf-8 -*-


def is_fraction_equivalent_pair(expr):
    r'''Is true when `expr` is an integer-equivalent pair of numbers 
    excluding ``0`` as the second term.

    ::

        >>> sequencetools.is_fraction_equivalent_pair((2, 3))
        True

    Otherwise false:

    ::

        >>> sequencetools.is_fraction_equivalent_pair((2, 0))
        False

    Returns boolean.
    '''
    from abjad.tools import sequencetools

    return sequencetools.is_integer_equivalent_pair(expr) and not expr[1] == 0
