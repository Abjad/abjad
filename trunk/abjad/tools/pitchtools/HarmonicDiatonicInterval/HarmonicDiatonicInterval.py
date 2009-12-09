from abjad.tools import mathtools
from abjad.tools.pitchtools._DiatonicInterval import _DiatonicInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval


class HarmonicDiatonicInterval(_DiatonicInterval, _HarmonicInterval):
   '''.. versionadded:: 1.1.2

   Harmonic diatonic interval. ::

      abjad> interval = pitchtools.HarmonicDiatonicInterval('minor', -3)
      abjad> interval
      HarmonicDiatonicInterval(minor third)
   '''

   def __init__(self, *args):
      if len(args) == 1 and isinstance(args[0], _DiatonicInterval):
         quality_string = args[0].quality_string
         number = abs(args[0].number)
      elif len(args) == 2:
         quality_string = args[0]
         number = abs(args[1])
      _DiatonicInterval.__init__(self, quality_string, number)

   ## OVERLOADS ##

   def __copy__(self):
      return HarmonicDiatonicInterval(
         self.quality_string, self.number)

   def __repr__(self):
      return _DiatonicInterval.__repr__(self)

   def __str__(self):
      return '%s%s' % (self._quality_abbreviation, self.number)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def counterpoint_interval(self):
      counterpoint_interval = self.interval_class
      if counterpoint_interval == 1:
         if self.number == 1:
            return 1
         else:
            return 8
      return counterpoint_interval

   @property
   def staff_spaces(self):
      if self.quality_string == 'perfect' and self.number == 1:
         return 0
      return abs(_DiatonicInterval.staff_spaces.fget(self))
