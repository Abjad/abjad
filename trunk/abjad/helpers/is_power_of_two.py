from abjad.rational.rational import Rational


def _is_power_of_two(expr):
   '''True when expr is an integer or Rational power of two,
      otherwise False.'''

   if isinstance(expr, int):
      return not bool(expr & (expr - 1))
   elif isinstance(expr, Rational):
      return _is_power_of_two(expr._n * expr._d)
   else:
      return False
