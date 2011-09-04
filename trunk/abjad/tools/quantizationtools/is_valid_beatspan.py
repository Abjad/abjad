from abjad import Fraction
from abjad.tools.durationtools import is_binary_rational
from abjad.tools.mathtools import is_nonnegative_integer_power_of_two


def is_valid_beatspan(beatspan):
    '''True if `beatspan` is a valid beatspan.

    1. A beatspan must be an int or Fraction.
    2. It must be a binary rational.
    3. If it is greater than zero, it must be a power of two.
    4. If it is less than zero, it must be Fraction, whose numerator is 1
        and whose denominator is a power of two.
    '''

    if is_binary_rational(beatspan) and 0 < beatspan:

        if beatspan == 1:
            return True

        if beatspan < 1:
            if beatspan.numerator == 1:
                if is_nonnegative_integer_power_of_two(beatspan.denominator):
                    return True

        if 1 < beatspan:
            if isinstance(beatspan, int):
                if is_nonnegative_integer_power_of_two(beatspan):
                    return True
            elif isinstance(beatspan, Fraction):
                if is_nonnegative_integer_power_of_two(beatspan.numerator):
                    if beatspan.denominator == 1:
                        return True

    return False
