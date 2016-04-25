# -*- coding: utf-8 -*-


def yield_all_pairs_between_sequences(l, m):
    '''Yields all pairs between sequences `l` and `m`.

    ::

        >>> for pair in sequencetools.yield_all_pairs_between_sequences([1, 2, 3], [4, 5]):
        ...     pair
        ...
        (1, 4)
        (1, 5)
        (2, 4)
        (2, 5)
        (3, 4)
        (3, 5)

    Returns generator.
    '''

    for x in l:
        for y in m:
            yield x, y
