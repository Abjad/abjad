def factors(n):
    """
    Gets prime factors less than or equal to ``n`` .

    ..  container:: example

        >>> abjad.mathtools.factors(84)
        [2, 2, 3, 7]

        >>> for n in range(10, 20):
        ...   print(n, abjad.mathtools.factors(n))
        ...
        10 [2, 5]
        11 [11]
        12 [2, 2, 3]
        13 [13]
        14 [2, 7]
        15 [3, 5]
        16 [2, 2, 2, 2]
        17 [17]
        18 [2, 3, 3]
        19 [19]

    ``n`` must be a positive integer.

    Returns factors in increasing order.

    Returns list of positive integers.
    """
    from abjad import mathtools
    if not mathtools.is_positive_integer(n):
        message = 'must be positive integer: {!r}.'
        message = message.format(n)
        raise TypeError(message)
    factor = 2
    factors = []
    while 1 < n:
        if n % factor == 0:
            factors.append(factor)
            n = n / factor
        else:
            factor = factor + 1
    return factors
