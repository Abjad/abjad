# -*- coding: utf-8 -*-
import collections


def get_shared_numeric_sign(argument):
    r'''Gets shared numeric sign of items in `argument`.

    ..  container:: example

        Returns ``1`` when all `argument` items are positive:

        ::

            >>> mathtools.get_shared_numeric_sign([1, 2, 3])
            1

        Returns ``-1`` when all `argument` items are negative:

        ::

            >>> mathtools.get_shared_numeric_sign([-1, -2, -3])
            -1

        Returns ``0`` on empty `argument`:

        ::

            >>> mathtools.get_shared_numeric_sign([])
            0

        Otherwise returns none:

        ::

            >>> mathtools.get_shared_numeric_sign([1, 2, -3]) is None
            True

    Returns ``1``, ``-1``, ``0`` or none.
    '''
    if not isinstance(argument, collections.Iterable):
        raise TypeError(argument)
    if len(argument) == 0:
        return 0
    elif all(0 < x for x in argument):
        return 1
    elif all(x < 0 for x in argument):
        return -1
    else:
        return None
