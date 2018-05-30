def least_common_multiple(*integers):
    """
    Gets least common multiple of positive ``integers``.

    ..  container:: example

        >>> abjad.mathtools.least_common_multiple(2, 4, 5, 10, 20)
        20

        >>> abjad.mathtools.least_common_multiple(4, 4)
        4

        >>> abjad.mathtools.least_common_multiple(4, 5)
        20

        >>> abjad.mathtools.least_common_multiple(4, 6)
        12

        >>> abjad.mathtools.least_common_multiple(4, 7)
        28

        >>> abjad.mathtools.least_common_multiple(4, 8)
        8

        >>> abjad.mathtools.least_common_multiple(4, 9)
        36

        >>> abjad.mathtools.least_common_multiple(4, 10)
        20

        >>> abjad.mathtools.least_common_multiple(4, 11)
        44

    Returns positive integer.
    """
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
    from abjad import mathtools
    assert isinstance(m, int), repr(m)
    assert isinstance(n, int), repr(n)
    factors_m = mathtools.factors(m)
    factors_n = mathtools.factors(n)
    for x in factors_m:
        try:
            factors_n.remove(x)
        except ValueError:
            pass
    result = 1
    for x in factors_m + factors_n:
        result *= x
    return result
