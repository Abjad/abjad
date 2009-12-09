from abjad.rational import Rational
from abjad.tools.pitchtools._ChromaticIntervalClass import \
   _ChromaticIntervalClass
from abjad.tools.pitchtools._HarmonicIntervalClass import \
   _HarmonicIntervalClass
from abjad.tools.pitchtools._Interval import _Interval


class HarmonicChromaticIntervalClass(_ChromaticIntervalClass,
   _HarmonicIntervalClass):
   '''.. versionadded:: 1.1.2

   Harmonic chromatic interval class.
   '''

   def __init__(self, token):
      if isinstance(token, (int, float, long, Rational)):
         number = token
      elif isinstance(_Interval):   
         number = token.semitones
      else:
         raise TypeError('must be number or interval instance.')
      if number % 12 == 0 and 12 <= abs(number):
         number = 12
      else:
         number = abs(number) % 12
      self._number = number
