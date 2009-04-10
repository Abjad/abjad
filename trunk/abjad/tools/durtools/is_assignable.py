from abjad.rational.rational import Rational
from abjad.tools import mathtools


def is_assignable(duration):
   '''Return True when duration 'duration' is rational-valued
      and of a form acceptable for assignment to written duration
      of a note, rest, chord or skip.

      That is, 'duration' must be a rational p/q,
      such that p/q is strictly greater than zero 
      and strictly less than 16, with denominator q
      a positive-valued power of two, and with numerator p
      of a form that can be written without recourse to ties.
      
      Otherwise False.'''

   duration = Rational(duration)
   return mathtools.is_power_of_two(duration._d) and \
      (0 < duration < 16) and \
      (not '01' in mathtools.binary_string(duration._n))
