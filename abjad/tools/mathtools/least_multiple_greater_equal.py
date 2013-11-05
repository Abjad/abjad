# -*- encoding: utf-8 -*-
import math


def least_multiple_greater_equal(m, n):
    r'''Returns the least integer multiple of `m`
    greater than or equal to `n`.

    ::

        >>> mathtools.least_multiple_greater_equal(10, 47)
        50

    ::

        >>> for m in range(1, 10):
        ...     print m, mathtools.least_multiple_greater_equal(m, 47)
        ...
        1 47
        2 48
        3 48
        4 48
        5 50
        6 48
        7 49
        8 48
        9 54

    ::

        >>> for n in range(10, 100, 10):
        ...     print mathtools.least_multiple_greater_equal(7, n), n
        ...
        14 10
        21 20
        35 30
        42 40
        56 50
        63 60
        70 70
        84 80
        91 90

    Returns integer.
    '''

    result = m * int(math.ceil(n / float(m)))

    return result
