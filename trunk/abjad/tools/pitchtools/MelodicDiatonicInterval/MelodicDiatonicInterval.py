from abjad.tools import mathtools
from abjad.tools.pitchtools._DiatonicInterval import _DiatonicInterval
from abjad.tools.pitchtools._MelodicInterval import _MelodicInterval
from abjad.tools.pitchtools.HarmonicDiatonicInterval import \
   HarmonicDiatonicInterval
from abjad.tools.pitchtools.HarmonicChromaticInterval import \
   HarmonicChromaticInterval
from abjad.tools.pitchtools.MelodicChromaticInterval import \
   MelodicChromaticInterval
from abjad.tools.pitchtools.MelodicCounterpointInterval import \
   MelodicCounterpointInterval
from abjad.tools.pitchtools.MelodicDiatonicIntervalClass import \
   MelodicDiatonicIntervalClass


class MelodicDiatonicInterval(_DiatonicInterval, _MelodicInterval):
   '''.. versionadded:: 1.1.2

   Melodic diatonic interval. ::

      abjad> interval = pitchtools.MelodicDiatonicInterval('minor', -3)
      abjad> interval
      MelodicDiatonicInterval(descending minor third)
   '''

   def __init__(self, *args):
      if len(args) == 1 and isinstance(args[0], MelodicDiatonicInterval):
         quality_string = args[0].quality_string
         number = args[0].number
      elif len(args) == 2:
         quality_string, number = args
      _DiatonicInterval.__init__(self, quality_string, number)

   ## OVERLOADS ##

   def __abs__(self):
      from abjad.tools.pitchtools.HarmonicDiatonicInterval import \
         HarmonicDiatonicInterval
      return HarmonicDiatonicInterval(
         self.quality_string, abs(self.number))

   def __neg__(self):
      return MelodicDiatonicInterval(self.quality_string, -self.number)

   def __repr__(self):
      if self.direction_string:
         return '%s(%s %s %s)' % (self.__class__.__name__, 
            self.direction_string, self.quality_string, self.interval_string)
      return _DiatonicInterval.__repr__(self)

   def __str__(self):
      return '%s%s%s' % (self._direction_symbol, self._quality_abbreviation,
         abs(self.number))
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def direction_number(self):
      if self.quality_string == 'perfect' and \
         abs(self.number) == 1:
         return 0
      else:
         return mathtools.sign(self.number)

   @property
   def direction_string(self):
      if self.direction_number == -1:
         return 'descending'
      elif self.direction_number == 0:
         return None
      elif self.direction_number == 1:
         return 'ascending'

   @property
   def harmonic_chromatic_interval(self):
      return HarmonicChromaticInterval(self)

   @property
   def harmonic_diatonic_interval(self):
      return HarmonicDiatonicInterval(self)

   @property
   def interval_class(self):
      #interval_class = _DiatonicInterval.interval_class.fget(self)
      #if self.number == 1:
      #   return 1
      #return self.direction_number * interval_class
      return MelodicDiatonicIntervalClass(self)

   @property
   def melodic_chromatic_interval(self):
      return MelodicChromaticInterval(self)

   @property
   def melodic_counterpoint_interval(self):
      return MelodicCounterpointInterval(self.number)

   @property
   def semitones(self):
      result = 0
      interval_class_number_to_semitones = {
         1: 0,  2: 1,  3: 3, 4: 5, 5: 7, 6: 8, 7: 10, 8: 0}
      interval_class_number = abs(self.interval_class.number)
      result += interval_class_number_to_semitones[interval_class_number]
      result += (abs(self.number) - 1) / 7 * 12
      quality_string_to_semitones = {
         'perfect': 0, 'major': 1, 'minor': 0, 'augmented': 1,
         'diminished': -1}
      result += quality_string_to_semitones[self.quality_string]
      if self.number < 0:
         result *= -1
      return result

   @property
   def staff_spaces(self):
      if self.direction_string == 'descending':
         return self.number + 1
      elif self.direction_string is None:
         return 0
      elif self.direction_string == 'ascending':
         return self.number - 1
