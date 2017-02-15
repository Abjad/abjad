# -*- coding: utf-8 -*-
import numbers


def is_negative_integer(argument):
    '''Is true when `argument` equals a negative integer. Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.is_negative_integer(-1)
            True

        ::

            >>> mathtools.is_negative_integer(0)
            False

        ::

            >>> mathtools.is_negative_integer(99)
            False

    Returns true or false.
    '''
    if isinstance(argument, numbers.Number):
        if argument == int(argument):
            if argument < 0:
                return True
    return False
