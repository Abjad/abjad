from abjad.tools.mathtools.factors import factors


def least_common_multiple(*integers):
    '''Least common multiple of positive `integers`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.least_common_multiple(2, 4, 5, 10, 20)
        20

    Return positive integer.
    '''

    if len(integers) == 1:
        if not isinstance(integers[0], int):
            raise TypeError('must be integer.')
        if not 0 < integers[0]:
            raise ValueError('must be positive.')
        return integers[0]

    cur_lcm = _least_common_multiple_helper(*integers[:2])
    for remaining_positive_integer in integers[2:]:
        cur_lcm = _least_common_multiple_helper(cur_lcm, remaining_positive_integer)
    return cur_lcm


def _least_common_multiple_helper(m, n):
    # check input
    if not isinstance(m, int):
        raise TypeError

    if not isinstance(n, int):
        raise TypeError

    # find factors of m and n
    factors_m = factors(m)
    factors_n = factors(n)

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
