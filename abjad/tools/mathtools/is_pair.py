# -*- coding: utf-8 -*-


def is_pair(argument):
    r'''Is true when `argument` is a tuple of length 2. Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.is_pair((19, 20))
            True

        ::

            >>> mathtools.is_pair((19, 20, 21))
            False

    Returns true or false.
    '''
    return isinstance(argument, tuple) and len(argument) == 2
