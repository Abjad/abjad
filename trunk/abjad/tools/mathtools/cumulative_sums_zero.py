def cumulative_sums_zero(sequence):
    '''Cumulative sums of `sequence` starting from ``0``:

    ::

        >>> mathtools.cumulative_sums_zero([1, 2, 3, 4, 5, 6, 7, 8])
        [0, 1, 3, 6, 10, 15, 21, 28, 36]

    Return ``[0]`` on empty `sequence`:

    ::

        >>> mathtools.cumulative_sums_zero([])
        [0]

    Return list.
    '''

    result = [0]
    for element in sequence:
        result.append(result[-1] + element)

    return result
