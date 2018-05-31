def is_positive_integer_power_of_two(argument):
    r"""
    Is true when ``argument`` is a positive integer power of 2.

    ..  container:: example

        >>> for n in range(10):
        ...     print(n, abjad.mathtools.is_positive_integer_power_of_two(n))
        ...
        0 False
        1 True
        2 True
        3 False
        4 True
        5 False
        6 False
        7 False
        8 True
        9 False

    Returns true or false.
    """
    from abjad import mathtools
    return (
        0 < argument and
        mathtools.is_nonnegative_integer_power_of_two(argument)
        )
