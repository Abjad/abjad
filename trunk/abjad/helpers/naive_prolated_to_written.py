from abjad.rational.rational import Rational
import math


def _naive_prolated_to_written(prolated_duration, prolation = 'diminution'):
   '''Return number of the form 1/2**n that is either just greater, 
      or just less, than prolated_duration, according to 'prolation'.

      Intended to find written duration of notes inside tuplet.

      _naive_prolated_to_written(Rational(3, 80), 'diminution')
      Rational(1, 32)

      _naive_prolated_to_written(Rational(3, 80), 'augmentation')
      Rational(1, 16)'''

   # find exponent of denominator
   if prolation == 'diminution':
      exponent = -int(math.ceil(math.log(prolated_duration, 2)))
   elif prolation == 'augmentation':
      exponent = -int(math.floor(math.log(prolated_duration, 2)))
   else:
      raise ValueError("must be 'diminution' or 'augmentation'.")

   # find numerator, denominator and written duration
   numerator = 1
   denominator = 2 ** exponent
   written_duration = Rational(numerator, denominator)

   # return written duration
   return written_duration
