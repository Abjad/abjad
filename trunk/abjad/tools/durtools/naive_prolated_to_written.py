from abjad.rational import Rational
import math


def naive_prolated_to_written(prolated_duration, prolation = 'diminution'):
   '''When ``prolation = 'diminution'`` return greatest rational of the form
   ``1/2**n`` that is less than or equal to `prolated_duration`. ::

      abjad> durtools.naive_prolated_to_written(Rational(3, 80), 'diminution')
      Rational(1, 32)

   When ``prolation = 'augmentation'`` return least rational of the form 
   ``1/2**n`` that is greater than or equal to `prolated_duration`. ::

      abjad> durtools.naive_prolated_to_written(Rational(3, 80), 'augmentation')
      Rational(1, 16)

   Function intended to find written duration of notes inside tuplet.
   '''

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
