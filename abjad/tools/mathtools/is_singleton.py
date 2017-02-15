# -*- coding: utf-8 -*-


def is_singleton(argument):
    r'''Is true when `argument` is a tuple of length 1. Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.is_singleton((19,))
            True

        ::

            >>> mathtools.is_singleton((19, 20, 21))
            False

    Returns true or false.
    '''
    return isinstance(argument, tuple) and len(argument) == 1
