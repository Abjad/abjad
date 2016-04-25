# -*- coding: utf-8 -*-


def get_shared_numeric_sign(sequence):
    r'''Gets shared numeric sign of elements in `sequence`.

    Returns ``1`` when all `sequence` elements are positive:

    ::

        >>> mathtools.get_shared_numeric_sign([1, 2, 3])
        1

    Returns ``-1`` when all `sequence` elements are negative:

    ::

        >>> mathtools.get_shared_numeric_sign([-1, -2, -3])
        -1

    Returns ``0`` on empty `sequence`:

    ::

        >>> mathtools.get_shared_numeric_sign([])
        0

    Otherwise returns none:

    ::

        >>> mathtools.get_shared_numeric_sign([1, 2, -3]) is None
        True

    Returns ``1``, ``-1``, ``0`` or none.
    '''

    if len(sequence) == 0:
        return 0
    elif all(0 < x for x in sequence):
        return 1
    elif all(x < 0 for x in sequence):
        return -1
    else:
        return None
