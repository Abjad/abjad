def is_positive_integer_power_of_two(expr):
    '''True when `expr` is a positive integer power of ``2``::

        >>> from abjad.tools import mathtools

    ::

        >>> for n in range(10):
        ...     print n, mathtools.is_positive_integer_power_of_two(n)
        ...
        0 False
        1 True
        2 True
        3 False
        4 True
        5 False
        6 False
        7 False
        8 True
        9 False

    Otherwise false.

    Return boolean.
    '''
    from abjad.tools import mathtools

    return 0 < expr and mathtools.is_nonnegative_integer_power_of_two(expr)
