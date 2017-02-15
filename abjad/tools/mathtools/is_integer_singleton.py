# -*- coding: utf-8 -*-


def is_integer_singleton(argument):
    r'''Is true when `argument` is an integer tuple of of length 1. Otherwise
    false.

    ..  container:: example

        ::

            >>> mathtools.is_integer_singleton((19,))
            True

        ::

            >>> mathtools.is_integer_singleton(('text',))
            False

    Returns true or false.
    '''
    return (
        isinstance(argument, tuple) and
        len(argument) == 1 and
        isinstance(argument[0], int)
        )
