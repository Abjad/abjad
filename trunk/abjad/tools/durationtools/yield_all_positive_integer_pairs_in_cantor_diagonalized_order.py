def yield_all_positive_integer_pairs_in_cantor_diagonalized_order():
    '''.. versionadded:: 2.0

    Yield all positive integer pairs in Cantor diagonalized order::

        abjad> from abjad.tools import durationtools

    ::

        abjad> generator = durationtools.yield_all_positive_integer_pairs_in_cantor_diagonalized_order()
        abjad> for n in range(16):
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
