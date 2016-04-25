# -*- coding: utf-8 -*-
import numbers


def are_relatively_prime(numbers_):
    '''Is true when `numbers_` is a sequence comprising zero or more numbers,
    all of which are relatively prime.

    ::

        >>> mathtools.are_relatively_prime([13, 14, 15])
        True

    Otherwise false:

    ::

        >>> mathtools.are_relatively_prime([13, 14, 15, 16])
        False

    Returns true when `numbers_` is an empty sequence:

    ::

        >>> mathtools.are_relatively_prime([])
        True

    Returns false when `numbers_` is nonsensical type:

    ::

        >>> mathtools.are_relatively_prime('foo')
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools

    if not all(isinstance(_, numbers.Number) for _ in numbers_):
        return False

    all_factors = set([])
    for number in numbers_:
        current_factors = mathtools.factors(number)
        current_factors = set(current_factors)
        if all_factors & current_factors:
            return False
        all_factors.update(current_factors)
    return True
