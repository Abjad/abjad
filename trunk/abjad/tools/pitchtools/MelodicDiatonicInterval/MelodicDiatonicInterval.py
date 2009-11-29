from abjad.tools import mathtools
from abjad.tools.pitchtools._DiatonicInterval import _DiatonicInterval
from abjad.tools.pitchtools._MelodicInterval import _MelodicInterval


class MelodicDiatonicInterval(_DiatonicInterval, _MelodicInterval):
   '''.. versionadded:: 1.1.2

   Melodic diatonic interval. ::

      abjad> interval = pitchtools.MelodicDiatonicInterval('minor', -3)
      abjad> interval
      MelodicDiatonicInterval(descending minor third)
   '''

   ## OVERLOADS ##

   def __abs__(self):
      from abjad.tools.pitchtools.HarmonicDiatonicInterval import \
         HarmonicDiatonicInterval
      return HarmonicDiatonicInterval(
         self.quality_string, abs(self.interval_number))

   def __neg__(self):
      return MelodicDiatonicInterval(self.quality_string, -self.interval_number)

   def __repr__(self):
      if self.direction_string:
         return '%s(%s %s %s)' % (self.__class__.__name__, 
            self.direction_string, self.quality_string, self.interval_string)
      return _DiatonicInterval.__repr__(self)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def direction_number(self):
      if self.quality_string == 'perfect' and \
         abs(self.interval_number) == 1:
         return 0
      else:
         return mathtools.sign(self.interval_number)

   @property
   def direction_string(self):
      if self.direction_number == -1:
         return 'descending'
      elif self.direction_number == 0:
         return None
      elif self.direction_number == 1:
         return 'ascending'

   @property
   def interval_class(self):
      interval_class = _DiatonicInterval.interval_class.fget(self)
      if self.interval_number == 1:
         return 1
      return self.direction_number * interval_class

   @property
   def semitones(self):
      result = 0
      interval_class_to_semitones = {
         1: 0,  2: 1,  3: 3, 4: 5, 5: 7, 6: 8, 7: 10}
      result += interval_class_to_semitones[abs(self.interval_class)]
      result += (abs(self.interval_number) - 1) / 7 * 12
      quality_string_to_semitones = {
         'perfect': 0, 'major': 1, 'minor': 0, 'augmented': 1,
         'diminished': -1}
      result += quality_string_to_semitones[self.quality_string]
      if self.interval_number < 0:
         result *= -1
      return result

   @property
   def staff_spaces(self):
      if self.direction_string == 'descending':
         return self.interval_number + 1
      elif self.direction_string is None:
         return 0
      elif self.direction_string == 'ascending':
         return self.interval_number - 1
