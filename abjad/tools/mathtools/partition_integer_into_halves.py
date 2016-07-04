# -*- coding: utf-8 -*-
import math


# TODO: replace string-valued even='allowed' with constant-valued keyword
def partition_integer_into_halves(n, bigger=Left, even='allowed'):
    r'''Writes positive integer `n` as the pair ``t = (left, right)``
    such that ``n == left + right``.

    When `n` is odd the greater part of ``t`` corresponds
    to the value of `bigger`:

    ::

        >>> mathtools.partition_integer_into_halves(7, bigger=Left)
        (4, 3)
        >>> mathtools.partition_integer_into_halves(7, bigger=Right)
        (3, 4)

    Likewise when `n` is even and ``even = 'disallowed'``:

    ::

        >>> mathtools.partition_integer_into_halves(
        ...     8,
        ...     bigger=Left,
        ...     even='disallowed',
        ...     )
        (5, 3)

    ::

        >>> mathtools.partition_integer_into_halves(
        ...     8,
        ...     bigger=Right,
        ...     even='disallowed',
        ...     )
        (3, 5)

    But when `n` is even and ``even = 'allowed'`` then ``left == right`` and
    `bigger` is ignored:

    ::

        >>> mathtools.partition_integer_into_halves(8)
        (4, 4)
        >>> mathtools.partition_integer_into_halves(8, bigger=Left)
        (4, 4)
        >>> mathtools.partition_integer_into_halves(8, bigger=Right)
        (4, 4)

    When `n` is ``0`` returns ``(0, 0)``:

    ::

        >>> mathtools.partition_integer_into_halves(0)
        (0, 0)

    When `n` is ``0`` and ``even = 'disallowed'`` raises partition error.

    Raises type error on noninteger `n`.

    Raises value error on negative `n`.

    Returns pair of positive integers.
    '''

    if not isinstance(n, int):
        raise TypeError

    if n < 0:
        raise ValueError

    if n == 0:
        if even == 'disallowed':
            raise Exception
        return (0, 0)

    smaller_half = int(math.floor(n / 2))
    bigger_half = n - smaller_half

    if (smaller_half == bigger_half) and (even != 'allowed'):
        smaller_half -= 1
        bigger_half += 1

    if bigger == Left:
        return (bigger_half, smaller_half)
    else:
        return (smaller_half, bigger_half)