# -*- coding: utf-8 -*-


def sign(n):
    r'''Returns ``-1`` on negative `n`:

    ::

        >>> mathtools.sign(-96.2)
        -1

    Returns ``0`` when `n` is ``0``:

    ::

        >>> mathtools.sign(0)
        0

    Returns ``1`` on positive `n`:

    ::

        >>> mathtools.sign(Duration(9, 8))
        1

    Returns ``-1``, ``0`` or ``1``.
    '''

    return (n > 0) - (n < 0)
