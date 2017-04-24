# -*- coding: utf-8 -*-


def is_null_tuple(argument):
    r'''Is true when `argument` is a tuple of length 0. Otherwise false.

    ..  container:: example

        ::

            >>> mathtools.is_null_tuple(())
            True

        ::

            >>> mathtools.is_null_tuple((19, 20, 21))
            False

    Returns true or false.
    '''
    return isinstance(argument, tuple) and not len(argument)
