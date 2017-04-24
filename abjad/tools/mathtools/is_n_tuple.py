# -*- coding: utf-8 -*-


def is_n_tuple(argument, n):
    r'''Is true when `argument` is a tuple of length `n`. Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.is_n_tuple((19, 20, 21), 3)
            True

        ::

            >>> mathtools.is_n_tuple((19, 20, 21), 4)
            False

    Returns true or false.
    '''
    return isinstance(argument, tuple) and len(argument) == n
