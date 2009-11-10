from abjad.rational import Rational
import math


def naive_prolated_to_written_not_greater_than(prolated_duration):
   '''Return greatest rational of the form ``1/2**n`` 
   that is less than or equal to `prolated_duration`. ::

      abjad> durtools.naive_prolated_to_written_not_greater_than(Rational(1, 80))
      Rational(1, 128)

   Function intended to find written duration of notes inside tuplet.
   '''

   # find exponent of denominator
   exponent = -int(math.floor(math.log(prolated_duration, 2)))

   # find numerator, denominator and written duration
   numerator = 1
   denominator = 2 ** exponent
   written_duration = Rational(numerator, denominator)

   # return written duration
   return written_duration
