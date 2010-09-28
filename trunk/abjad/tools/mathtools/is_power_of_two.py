from abjad.core import Fraction


def is_power_of_two(expr):
   '''``True`` when expr is an integer or rational power of ``2``,
   otherwise ``False``.
   
   ::

      abjad> for n in range(10):
      ...     print n, mathtools.is_power_of_two(n)
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

   ::

      abjad> mathtools.is_power_of_two(-4)
      False

   ::

      abjad> mathtools.is_power_of_two('foo')
      False
   '''

      

   if isinstance(expr, (int, long)):
      return not bool(expr & (expr - 1))
   elif isinstance(expr, Fraction):
      return is_power_of_two(expr.numerator * expr.denominator)
   else:
      return False
