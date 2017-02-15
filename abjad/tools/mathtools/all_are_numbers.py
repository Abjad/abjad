# -*- coding: utf-8 -*-
import numbers


def all_are_numbers(argument):
    '''Is true when `argument` is an iterable collection of numbers.
    Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.all_are_numbers([1, 2, 3.0, Fraction(13, 8)])
            True

        ::

            >>> mathtools.all_are_numbers(17)
            False

    ..  container:: example

        Is true when `argument` is empty:

        ::

            >>> mathtools.all_are_numbers([])
            True

    Returns true or false.
    '''
    try:
        return all(isinstance(_, numbers.Number) for _ in argument)
    except TypeError:
        return False
