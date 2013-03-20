def difference_series(sequence):
    '''Difference series of `sequence`:

    ::

        >>> mathtools.difference_series([1, 1, 2, 3, 5, 5, 6])
        [0, 1, 1, 2, 0, 1]

    Return list.
    '''

    result = []

    for i, n in enumerate(sequence[1:]):
        result.append(n - sequence[i])

    return result
