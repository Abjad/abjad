def yield_all_positive_integer_pairs():
    '''.. versionadded:: 2.0

    Yield all positive integer pairs in Cantor diagonalized order::

        >>> from abjad.tools import durationtools

    ::

        >>> generator = durationtools.yield_all_positive_integer_pairs()
        >>> for n in range(16):
        ...     generator.next()
        ...
        (1, 1)
        (2, 1)
        (1, 2)
        (1, 3)
        (2, 2)
        (3, 1)
        (4, 1)
        (3, 2)
        (2, 3)
        (1, 4)
        (1, 5)
        (2, 4)
        (3, 3)
        (4, 2)
        (5, 1)
        (6, 1)

    Return pair generator.
    '''

    n = 2
    while True:
        if n % 2 == 0:
            lhs = 1
            while lhs < n:
                rhs = n - lhs
                yield lhs, rhs
                lhs += 1
        else:
            lhs = n - 1
            while 0 < lhs:
                rhs = n - lhs
                yield lhs, rhs
                lhs -= 1
        n += 1
