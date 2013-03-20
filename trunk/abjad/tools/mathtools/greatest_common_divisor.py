def greatest_common_divisor(*integers):
    '''.. versionadded:: 2.0

    Calculate greatest common divisor of `integers`:

    ::

        >>> mathtools.greatest_common_divisor(84, -94, -144)
        2

    Allow nonpositive input.

    Raise type error on noninteger input.

    Raise not implemented error when ``0`` is included in input.

    Return positive integer.
    '''
    from abjad.tools import mathtools

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
