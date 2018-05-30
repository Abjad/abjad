import collections
from abjad import Fraction


def arithmetic_mean(argument):
    """
    Gets arithmetic mean of ``argument``.

    ..  container:: example

        >>> abjad.mathtools.arithmetic_mean([1, 2, 2, 20, 30])
        11

        >>> abjad.mathtools.arithmetic_mean([1, 2, 20])
        Fraction(23, 3)

        >>> abjad.mathtools.arithmetic_mean([2, 2, 20.0])
        8.0

    Raises exception when ``argument`` is not iterable.

    Returns number.
    """
    if not isinstance(argument, collections.Iterable):
        raise TypeError(argument)
    total = sum(argument)
    length = len(argument)
    if isinstance(total, float):
        return total / length
    result = Fraction(sum(argument), len(argument))
    int_result = int(result)
    if int_result == result:
        return int_result
    else:
        return result
