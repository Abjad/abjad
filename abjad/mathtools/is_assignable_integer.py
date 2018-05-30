def is_assignable_integer(argument):
    r"""
    Is true when ``argument`` is equivalent to an integer that can be written
    without recourse to ties.

    ..  container:: example

        >>> for n in range(0, 16 + 1):
        ...     print('%s\t%s' % (n, abjad.mathtools.is_assignable_integer(n)))
        ...
        0  False
        1  True
        2  True
        3  True
        4  True
        5  False
        6  True
        7  True
        8  True
        9  False
        10 False
        11 False
        12 True
        13 False
        14 True
        15 True
        16 True

    Returns true or false.
    """
    from abjad import mathtools
    if isinstance(argument, int):
        if 0 < argument:
            if '01' not in mathtools.integer_to_binary_string(argument):
                return True
    return False
