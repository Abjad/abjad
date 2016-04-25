# -*- coding: utf-8 -*-


def factors(n):
    r'''Prime factors less than or equal to positive integer `n` 
    in increasing order.

    ..  container:: example

        **Example 1.** Factors 84: 

        ::

            >>> mathtools.factors(84)
            [2, 2, 3, 7]

    ..  container:: example

        **Example 2.** Factors the number 10 through 19, inclusive:

        ::

            >>> for n in range(10, 20):
            ...   print(n, mathtools.factors(n))
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

    Raises type error on noninteger `n`.

    Raises value error on nonpositive `n`.

    Returns list of one or more positive integers.
    '''
    from abjad.tools import mathtools

    if not mathtools.is_positive_integer(n):
        message = 'must be positive integer: {!r}.'
        message = message.format(n)
        raise TypeError(message)

    d = 2
    factors = []
    while 1 < n:
        if n % d == 0:
            factors.append(d)
            n = n/d
        else:
            d = d + 1
    return factors
