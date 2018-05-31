import math


def integer_to_base_k_tuple(n, k):
    """
    Changes nonnegative integer ``n`` to base-`k` tuple.

    ..  container:: example

        Gets base-10 digits of 1066:

        >>> abjad.mathtools.integer_to_base_k_tuple(1066, 10)
        (1, 0, 6, 6)

    ..  container:: example

        Gets base-2 digits of 1066:

        >>> abjad.mathtools.integer_to_base_k_tuple(1066, 2)
        (1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0)

    ..  container:: example

        Gets base-26 digits of 1066:

        >>> abjad.mathtools.integer_to_base_k_tuple(1066, 26)
        (1, 15, 0)

    Returns tuple of positive integers.
    """
    assert isinstance(n, int), repr(n)
    assert 0 <= n, repr(n)
    if n == 0:
        return (0,)
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
