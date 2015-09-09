# -*- coding: utf-8 -*-


def remove_powers_of_two(n):
    r'''Removes powers of ``2`` from the factors of positive integer `n`:

    ::

        >>> for n in range(10, 100, 10):
        ...     print('\t%s\t%s' % (n, mathtools.remove_powers_of_two(n)))
        ... 
            10 5
            20 5
            30 15
            40 5
            50 25
            60 15
            70 35
            80 5
            90 45

    Raises type error on noninteger `n`.

    Raises value error on nonpositive `n`.

    Returns positive integer.
    '''

    if not isinstance(n, int):
        raise TypeError

    if n <= 0:
        raise ValueError

    while n % 2 == 0:
        n //= 2

    return n
