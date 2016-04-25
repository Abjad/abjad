# -*- coding: utf-8 -*-


def yield_all_partitions_of_integer(n):
    r'''Yields all partitions of positive integer `n` in descending lex order:

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

    Returns generator of positive integer tuples of length at least ``1``.
    '''
    from abjad.tools import mathtools

    if not isinstance(n, int):
        message = 'must be integer.'
        raise TypeError(message)
    if not 0 < n:
        message = 'must be positive.'
        raise ValueError(message)

    partition = (n, )
    while partition is not None:
        yield partition
        partition = mathtools.next_integer_partition(partition)
