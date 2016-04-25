# -*- coding: utf-8 -*-


def least_common_multiple(*integers):
    r'''Least common multiple of positive `integers`.

    ::

        >>> mathtools.least_common_multiple(2, 4, 5, 10, 20)
        20

    Returns positive integer.
    '''
    from abjad.tools import mathtools

    if len(integers) == 1:
        if not isinstance(integers[0], int):
            message = 'must be integer: {!r}.'
            message = message.format(integers[0])
            raise TypeError(message)
        if not 0 < integers[0]:
            message = 'must be positive: {!r}.'
            message = message.format(integers[0])
            raise ValueError(message)
        return integers[0]

    current_lcm = _least_common_multiple_helper(*integers[:2])
    for remaining_positive_integer in integers[2:]:
        current_lcm = _least_common_multiple_helper(
            current_lcm, remaining_positive_integer)
    return current_lcm


def _least_common_multiple_helper(m, n):
    from abjad.tools import mathtools

    # check input
    if not isinstance(m, int):
        raise TypeError

    if not isinstance(n, int):
        raise TypeError

    # find factors of m and n
    factors_m = mathtools.factors(m)
    factors_n = mathtools.factors(n)

    # remove duplicated shared factors
    for x in factors_m:
        try:
            factors_n.remove(x)
        except ValueError:
            pass

    # calculate product of shared factors
    result = 1
    for x in factors_m + factors_n:
        result *= x

    # return product
    return result
