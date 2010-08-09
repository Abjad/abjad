from abjad.core import Rational
from abjad.tools import mathtools
from abjad.tools.pitchtools._ChromaticIntervalClass import _ChromaticIntervalClass
from abjad.tools.pitchtools._Interval import _Interval
from abjad.tools.pitchtools._IntervalClass import _IntervalClass
from abjad.tools.pitchtools._MelodicIntervalClass import _MelodicIntervalClass


class MelodicChromaticIntervalClass(_ChromaticIntervalClass,
   _MelodicIntervalClass):
   '''.. versionadded:: 1.1.2

   Melodic chromatic interval class.
   '''

   def __init__(self, token):
      if isinstance(token, (int, float, long, Rational)):
         sign = mathtools.sign(token)
         abs_token = abs(token)
         if abs_token % 12 == 0 and 12 <= abs_token:
            self._number = 12
         else:
            self._number = abs_token % 12
         self._number *= sign
      elif isinstance(token, _Interval):
         number = token.semitones
         sign = mathtools.sign(number)
         abs_number = abs(number)
         if abs_number % 12 == 0 and 12 <= abs_number:
            self._number = 12
         else:
            self._number = abs_number % 12
         self._number *= sign
      elif isinstance(token, _IntervalClass):
         number = token.number
         sign = mathtools.sign(number)
         abs_number = abs(number)
         if abs_number % 12 == 0 and 12 <= abs_number:
            self._number = 12
         else:
            self._number = abs_number % 12
         self._number *= sign
      else:
         raise ValueError('must be number, interval or interval class.')

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, MelodicChromaticIntervalClass):
         if self.number == arg.number:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg
