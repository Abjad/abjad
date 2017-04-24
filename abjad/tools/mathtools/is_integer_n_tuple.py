# -*- coding: utf-8 -*-


def is_integer_n_tuple(argument, n):
    r'''Is true when `argument` is an integer tuple of length `n`.
    Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.is_integer_n_tuple((19, 20, 21), 3)
            True

        ::

            >>> mathtools.is_integer_n_tuple((19, 20, 'text'), 3)
            False

    Returns true or false.
    '''

    return (
        isinstance(argument, tuple) and
        len(argument) == n and
        all(isinstance(_, int) for _ in argument)
        )
