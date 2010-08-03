from abjad.Pitch import Pitch
from abjad.tools.pitchtools._DiatonicIntervalClass import _DiatonicIntervalClass
from abjad.tools.pitchtools._HarmonicIntervalClass import \
   _HarmonicIntervalClass


class HarmonicDiatonicIntervalClass(
   _DiatonicIntervalClass, _HarmonicIntervalClass):
   '''.. versionadded:: 1.1.2

   Harmonic diatonic interval class.
   '''

   def __init__(self, *args):
      from abjad.tools.pitchtools.HarmonicDiatonicInterval import \
         HarmonicDiatonicInterval
      if len(args) == 1:
         if isinstance(args[0], HarmonicDiatonicInterval):
            quality_string = args[0]._quality_string
            number = args[0].number
         elif isinstance(args[0], tuple) and len(args[0]) == 2:
            quality_string, number = args[0]
         else:
            raise TypeError
      else:
         quality_string, number = args   
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
         if number == 0:
            number = 7
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

   ## PUBLIC METHODS ##

   def invert(self):
      from abjad.tools.pitchtools.MelodicDiatonicInterval import \
         MelodicDiatonicInterval
      from abjad.tools.pitchtools.harmonic_diatonic_interval_class_from_to \
         import harmonic_diatonic_interval_class_from_to
      low = Pitch('c', 4)
      quality_string, number = self._quality_string, self.number
      mdi = MelodicDiatonicInterval(quality_string, number)
      middle = low + mdi
      octave = MelodicDiatonicInterval('perfect', 8)
      high = low + octave
      hdi = harmonic_diatonic_interval_class_from_to(middle, high)
      return hdi
