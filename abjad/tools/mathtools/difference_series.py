# -*- coding: utf-8 -*-


def difference_series(sequence):
    r'''Gets difference series of `sequence`.

    **Example 1.** Monotonically increasing:

    ::

        >>> mathtools.difference_series([1, 1, 2, 3, 5, 5, 6])
        [0, 1, 1, 2, 0, 1]

    **Example 2.** Alternating direction:

    ::

        >>> mathtools.difference_series([9, 6, 8, 5, 7, 4, 6])
        [-3, 2, -3, 2, -3, 2]

    Returns list.
    '''
    result = []
    for i, n in enumerate(sequence[1:]):
        result.append(n - sequence[i])
    return result