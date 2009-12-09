from abjad.rational import Rational
from abjad.tools.pitchtools._ChromaticIntervalClass import \
   _ChromaticIntervalClass
from abjad.tools.pitchtools._MelodicIntervalClass import \
   _MelodicIntervalClass


class MelodicChromaticIntervalClass(_ChromaticIntervalClass,
   _MelodicIntervalClass):
   '''.. versionadded:: 1.1.2

   Melodic chromatic interval class.
   '''

   def __init__(self, token):
      if isinstance(token, (int, float, long, Rational)):
         if token % 12 == 0 and 12 <= abs(token):
            self._number = 12
         else:
            self._number = token % 12
      elif isinstance(_Interval):
         number = token.semitones
         if number % 12 == 0 and 12 <= abs(number):
            self._number = 12
         else:
            self._number = number % 12
      else:
         raise ValueError('must be number or interval instance.')
