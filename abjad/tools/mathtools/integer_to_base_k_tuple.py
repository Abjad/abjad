# -*- coding: utf-8 -*-
import math


def integer_to_base_k_tuple(n, k):
    '''Nonnegative integer `n` to base-`k` tuple.

    ::

        >>> mathtools.integer_to_base_k_tuple(1066, 10)
        (1, 0, 6, 6)

    Returns tuple of one or more positive integers.
    '''

    if not isinstance(n, int):
        raise TypeError

    if not 0 <= n:
        raise ValueError

    if n == 0:
        return (0, )

    result = []
    current_exponent = math.trunc(math.log(n, k))
    remainder = n
    while 0 <= current_exponent:
        current_power = k ** current_exponent
        current_digit = remainder // current_power
        result.append(current_digit)
        remainder -= current_digit * current_power
        current_exponent -= 1
    return tuple(result)
