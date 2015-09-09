# -*- coding: utf-8 -*-


# TODO: function should return nonreduced fraction generator instead
#       of pair generator.
def yield_nonreduced_fractions():
    '''Yields positive nonreduced fractions in Cantor diagonalized order:

    ::

        >>> generator = mathtools.yield_nonreduced_fractions()
        >>> for n in range(16):
        ...     next(generator)
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

    Returns generator.
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
