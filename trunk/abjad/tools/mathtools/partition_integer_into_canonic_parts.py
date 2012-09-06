def partition_integer_into_canonic_parts(n, big_endian=True):
    '''Partition integer `n` into big-endian or small-endian parts.

    Return all parts positive on positive `n`::

        >>> for n in range(1, 11):
        ...     print n, mathtools.partition_integer_into_canonic_parts(n)
        ...
        1 (1,)
        2 (2,)
        3 (3,)
        4 (4,)
        5 (4, 1)
        6 (6,)
        7 (7,)
        8 (8,)
        9 (8, 1)
        10 (8, 2)

    Return all parts negative on negative `n`::

        >>> for n in reversed(range(-20, -10)):
        ...     print n, mathtools.partition_integer_into_canonic_parts(n)
        ...
        -11 (-8, -3)
        -12 (-12,)
        -13 (-12, -1)
        -14 (-14,)
        -15 (-15,)
        -16 (-16,)
        -17 (-16, -1)
        -18 (-16, -2)
        -19 (-16, -3)
        -20 (-16, -4)

    Return little-endian tuple::

        >>> for n in range(11, 21):
        ...     print n, mathtools.partition_integer_into_canonic_parts(n, big_endian=False)
        ...
        11 (3, 8)
        12 (12,)
        13 (1, 12)
        14 (14,)
        15 (15,)
        16 (16,)
        17 (1, 16)
        18 (2, 16)
        19 (3, 16)
        20 (4, 16)

    Return big-endian tuple ``t = (t_0, ..., t_j)`` such that

        *  ``sum(t) == n``
        *  ``t_i`` can be written without recourse to ties, and
        *  ``t_(i + 1) < t_i`` for every ``t_i`` in ``t``.

    Raise type error on noninteger `n`.

    Return tuple of one or more integers.
    '''
    from abjad.tools import mathtools

    if not isinstance(n, (int, long)):
        raise TypeError

    if not isinstance(big_endian, bool):
        raise ValueError

    if n == 0:
        return (0, )

    result = []
    prev_empty = True
    binary_n = mathtools.integer_to_binary_string(abs(n))
    binary_length = len(binary_n)

    for i, x in enumerate(binary_n):
        if x == '1':
            place_value = 2 ** (binary_length - i - 1)
            if prev_empty:
                result.append(place_value)
            else:
                result[-1] += place_value
            prev_empty = False
        else:
            prev_empty = True

    sign_n = mathtools.sign(n)
    if mathtools.sign(n) == -1:
        result = [sign_n * x for x in result]

    if big_endian:
        return tuple(result)
    else:
        return tuple(reversed(result))
