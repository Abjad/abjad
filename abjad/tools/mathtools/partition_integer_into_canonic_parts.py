# -*- encoding: utf-8 -*-


def partition_integer_into_canonic_parts(n, decrease_parts_monotonically=True):
    r'''Partitions integer `n` into canonic parts.

    Returns all parts positive on positive `n`:

    ::

        >>> for n in range(1, 11):
        ...     print(n, mathtools.partition_integer_into_canonic_parts(n))
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

    Returns all parts negative on negative `n`:

    ::

        >>> for n in reversed(range(-20, -10)):
        ...     print(n, mathtools.partition_integer_into_canonic_parts(n))
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

    Returns parts that increase monotonically:

    ::

        >>> for n in range(11, 21):
        ...     print(n, mathtools.partition_integer_into_canonic_parts(n,
        ...         decrease_parts_monotonically=False))
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

    Returns tuple with parts that decrease monotonically.

    Raises type error on noninteger `n`.

    Returns tuple of one or more integers.
    '''
    from abjad.tools import mathtools

    if not isinstance(n, int):
        raise TypeError

    if not isinstance(decrease_parts_monotonically, bool):
        raise ValueError

    if n == 0:
        return (0, )

    result = []
    previous_empty = True
    binary_n = mathtools.integer_to_binary_string(abs(n))
    binary_length = len(binary_n)

    for i, x in enumerate(binary_n):
        if x == '1':
            place_value = 2 ** (binary_length - i - 1)
            if previous_empty:
                result.append(place_value)
            else:
                result[-1] += place_value
            previous_empty = False
        else:
            previous_empty = True

    sign_n = mathtools.sign(n)
    if mathtools.sign(n) == -1:
        result = [sign_n * x for x in result]

    if decrease_parts_monotonically:
        return tuple(result)
    else:
        return tuple(reversed(result))
