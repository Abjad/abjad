# -*- encoding: utf-8 -*-
import math


def divisors(n):
    r'''Positive divisors of integer `n` in increasing order.

    ::

        >>> mathtools.divisors(84)
        [1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84]

    ::

        >>> for x in range(10, 20):
        ...     print(x, mathtools.divisors(x))
        ... 
        10 [1, 2, 5, 10]
        11 [1, 11]
        12 [1, 2, 3, 4, 6, 12]
        13 [1, 13]
        14 [1, 2, 7, 14]
        15 [1, 3, 5, 15]
        16 [1, 2, 4, 8, 16]
        17 [1, 17]
        18 [1, 2, 3, 6, 9, 18]
        19 [1, 19]

    Allows nonpositive `n`:

    ::

        >>> mathtools.divisors(-27)
        [1, 3, 9, 27]

    Raises type error on noninteger `n`.

    Raises not implemented error on ``0``.

    Returns list of positive integers.
    '''

    if not isinstance(n, int):
        message = 'must be integer: {!r}.'
        message = message.format(n)
        raise TypeError(message)

    if n == 0:
        message = 'all numbers divide zero evenly.'
        raise NotImplementedError(message)

    # ensure positive n
    n = abs(n)

    # find all divisors from 1 to sqrt(n)
    divisors = [1]
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)

    # find codivisors
    codivisors = [n // i for i in reversed(divisors)]

    # remove duplciate divisor if n is perfect square
    if divisors[-1] == codivisors[0]:
        divisors.pop()

    # extend and sort divisors
    divisors.extend(codivisors)
    divisors.sort()

    # return divisors
    return divisors
