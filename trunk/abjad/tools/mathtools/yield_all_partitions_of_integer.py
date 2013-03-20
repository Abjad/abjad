def yield_all_partitions_of_integer(n):
    r'''.. versionadded:: 2.0

    Yield all partitions of positive integer `n` in descending lex order:

    ::

        >>> for partition in mathtools.yield_all_partitions_of_integer(7):
        ...     partition
        ...
        (7,)
        (6, 1)
        (5, 2)
        (5, 1, 1)
        (4, 3)
        (4, 2, 1)
        (4, 1, 1, 1)
        (3, 3, 1)
        (3, 2, 2)
        (3, 2, 1, 1)
        (3, 1, 1, 1, 1)
        (2, 2, 2, 1)
        (2, 2, 1, 1, 1)
        (2, 1, 1, 1, 1, 1)
        (1, 1, 1, 1, 1, 1, 1)

    Return generator of positive integer tuples of length at least ``1``.
    '''
    from abjad.tools import mathtools

    if not isinstance(n, int):
        raise TypeError('must be integer.')
    if not 0 < n:
        raise ValueError('must be positive.')

    partition = (n, )
    while partition is not None:
        yield partition
        partition = mathtools.next_integer_partition(partition)
