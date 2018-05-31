def greatest_common_divisor(*integers):
    """
    Calculates greatest common divisor of ``integers``.

    ..  container:: example

        >>> abjad.mathtools.greatest_common_divisor(84, -94, -144)
        2

    Allows nonpositive input.

    Raises not implemented error when zero is included in input.

    Returns positive integer.
    """
    from abjad import mathtools
    common_divisors = None
    for positive_integer in integers:
        all_divisors = set(mathtools.divisors(positive_integer))
        if common_divisors is None:
            common_divisors = all_divisors
        else:
            common_divisors &= all_divisors
            if common_divisors == set([1]):
                return 1
    return max(common_divisors)
