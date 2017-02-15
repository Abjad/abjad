# -*- coding: utf-8 -*-
import collections


def cumulative_signed_weights(argument):
    r'''Gets cumulative signed weights of `argument`.

    ..  container:: example

        ::

            >>> argument = [1, -2, -3, 4, -5, -6, 7, -8, -9, 10]
            >>> mathtools.cumulative_signed_weights(argument)
            [1, -3, -6, 10, -15, -21, 28, -36, -45, 55]

        ::

            >>> argument = [-1, -2, -3, -4, -5, 0, 0, 0, 0, 0]
            >>> mathtools.cumulative_signed_weights(argument)
            [-1, -3, -6, -10, -15, -15, -15, -15, -15, -15]

        ::

            >>> argument = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            >>> mathtools.cumulative_signed_weights(argument)
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    Raises type error when `argument` is not iterable.

    Returns new object of `argument` type.
    '''
    from abjad.tools import mathtools
    if not isinstance(argument, collections.Iterable):
        raise TypeError(argument)
    result = []
    for item in argument:
        try:
            next_element = abs(previous) + abs(item)
            previous_sign = mathtools.sign(previous)
        except NameError:
            next_element = abs(item)
            previous_sign = 0
        sign = mathtools.sign(item)
        if sign == -1:
            next_element *= sign
        elif sign == 0:
            next_element *= previous_sign
        result.append(next_element)
        previous = next_element
    return result
