from abjad.tools.mathtools.next_integer_partition import next_integer_partition


def yield_all_partitions_of_integer(n):
    r'''.. versionadded:: 2.0

    Yield all partitions of positive integer `n` in descending lex order::

        abjad> from abjad.tools import mathtools

    ::

        abjad> for partition in mathtools.yield_all_partitions_of_integer(7):
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

    .. versionchanged:: 2.0
        renamed ``mathtools.integer_partitions()`` to
        ``mathtools.yield_all_partitions_of_integer()``.
    '''

    if not isinstance(n, int):
        raise TypeError('must be integer.')
    if not 0 < n:
        raise ValueError('must be positive.')

    partition = (n, )
    while partition is not None:
        yield partition
        partition = next_integer_partition(partition)

    #raise StopIteration
