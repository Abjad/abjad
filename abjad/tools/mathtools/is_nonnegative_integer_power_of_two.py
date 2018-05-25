from abjad import Fraction


def is_nonnegative_integer_power_of_two(argument) -> bool:
    """
    Is true when ``argument`` is a nonnegative integer power of 2.

    ..  container:: example

        >>> for n in range(10):
        ...     print(n, abjad.mathtools.is_nonnegative_integer_power_of_two(n))
        ...
        0 True
        1 True
        2 True
        3 False
        4 True
        5 False
        6 False
        7 False
        8 True
        9 False

    """
    if isinstance(argument, int):
        return not bool(argument & (argument - 1))
    elif isinstance(argument, Fraction):
        return is_nonnegative_integer_power_of_two(
            argument.numerator * argument.denominator
            )
    else:
        return False
