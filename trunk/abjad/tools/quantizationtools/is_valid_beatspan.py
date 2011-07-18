from abjad import Fraction
from abjad.tools.durtools import is_binary_rational
from abjad.tools.mathtools import is_nonnegative_integer_power_of_two


def is_valid_beatspan(beatspan):
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
