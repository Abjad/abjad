# -*- coding: utf-8 -*-
import math
from abjad import Fraction


def least_power_of_two_greater_equal(n, i=0):
    r'''Gets least integer power of two greater than or equal to positive `n`.

    ..  container:: example

        ::

            >>> for n in range(10, 20):
            ...     print('\t%s\t%s' % (n, mathtools.least_power_of_two_greater_equal(n)))
            ... 
            10 16
            11 16
            12 16
            13 16
            14 16
            15 16
            16 16
            17 32
            18 32
            19 32

    ..  container:: example

        When ``i = 1``, returns the first integer power of 2 greater than the
        least integer power of 2 greater than or equal to `n`.

        ::

            >>> for n in range(10, 20):
            ...     print('\t%s\t%s' % (n, mathtools.least_power_of_two_greater_equal(n, i=1)))
            ... 
            10 32
            11 32
            12 32
            13 32
            14 32
            15 32
            16 32
            17 64
            18 64
            19 64

    When ``i = 2``, returns the second integer power of 2 greater than the
    least integer power of 2 greater than or equal to `n`, and, in general,
    return the ``i`` th integer power of 2 greater than the least integer power
    of 2 greater than or equal to `n`.

    Returns integer.
    '''
    if not isinstance(n, (int, float, Fraction)):
        raise TypeError
    if n <= 0:
        raise ValueError
    result = 2 ** (int(math.ceil(math.log(n, 2))) + i)
    return result
