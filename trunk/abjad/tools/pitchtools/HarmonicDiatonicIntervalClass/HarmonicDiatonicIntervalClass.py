from abjad.tools.pitchtools._DiatonicIntervalClass import _DiatonicIntervalClass
from abjad.tools.pitchtools._HarmonicIntervalClass import \
   _HarmonicIntervalClass


class HarmonicDiatonicIntervalClass(
   _DiatonicIntervalClass, _HarmonicIntervalClass):
   '''.. versionadded:: 1.1.2

   Harmonic diatonic interval class.
   '''

   def __init__(self, quality_string, number):
      if quality_string not in self._acceptable_quality_strings:
         raise ValueError('not acceptable quality string.')
      self._quality_string = quality_string
      if not isinstance(number, int):
         raise TypeError('must be integer.')
      if number == 0:
         raise ValueError('must be nonzero.')
      abs_number = abs(number)
      if abs_number % 7 == 1 and 8 <= abs_number:
         number = 8
      else:
         number = abs_number % 7
      self._number = number

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, HarmonicDiatonicIntervalClass):
         if self._quality_string == arg._quality_string:
            if self.number == arg.number:
               return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __str__(self):
      return '%s%s' % (self._quality_abbreviation, self.number)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _full_name(self):
      return '%s %s' % (self._quality_string, self._interval_string)
