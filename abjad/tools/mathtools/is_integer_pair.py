# -*- coding: utf-8 -*-


def is_integer_pair(argument):
    r'''Is true when `argument` is an integer tuple of length 2. Otherwise
    false.

    ..  container:: example

        ::

            >>> mathtools.is_integer_pair((19, 20))
            True

        ::

            >>> mathtools.is_integer_pair(('some', 'text'))
            False

    Returns true or false.
    '''
    return (
        isinstance(argument, tuple) and
        len(argument) == 2 and
        all(isinstance(_, int) for _ in argument)
        )
