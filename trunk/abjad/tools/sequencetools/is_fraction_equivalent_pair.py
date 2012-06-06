from abjad.tools.sequencetools.is_integer_equivalent_pair import is_integer_equivalent_pair


def is_fraction_equivalent_pair(expr):
    r'''.. versionadded:: 2.9

    True when `expr` is an integer-equivalent pair of numbers excluding ``0`` as the second term::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.is_fraction_equivalent_pair((2, 3))
        True

    Otherwise false::

        >>> sequencetools.is_fraction_equivalent_pair((2, 0))
        False

    Return boolean.
    '''

    return is_integer_equivalent_pair(expr) and not expr[1] == 0
