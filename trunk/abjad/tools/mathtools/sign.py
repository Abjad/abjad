def sign(n):
    '''Return ``-1`` on negative `n`::

        >>> mathtools.sign(-96.2)
        -1

    Return ``0`` when `n` is ``0``::

        >>> mathtools.sign(0)
        0

    Return ``1`` on positive `n`::

        >>> mathtools.sign(Duration(9, 8))
        1

    Return ``-1``, ``0`` or ``1``.
    '''

    return cmp(n, 0)
