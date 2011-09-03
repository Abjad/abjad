import math


def integer_to_base_k_tuple(n, k):
    '''.. versionadded:: 2.0

    Nonnegative integer `n` to base-`k` tuple::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.integer_to_base_k_tuple(1066, 10)
        (1, 0, 6, 6)

    Return tuple of one or more positive integers.
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
