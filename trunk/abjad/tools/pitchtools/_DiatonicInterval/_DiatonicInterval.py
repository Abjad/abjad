from abjad.tools import mathtools
from abjad.tools.pitchtools._Interval import _Interval


class _DiatonicInterval(_Interval):
   '''.. versionadded:: 1.1.2

   Abstract diatonic interval class from which concrete classes inherit.
   '''

   def __init__(self, quality_string, interval_number):
      if quality_string in self._acceptable_quality_strings:
         self._quality_string = quality_string
      else:
         raise ValueError("quality string '%s' must be in %s." % (
            quality_string, str(self._acceptable_quality_strings)))
      if isinstance(interval_number, int):
         if int == 0:
            raise ValueError
         self._interval_number = interval_number
      else:
         raise ValueError('interval must be integer.')

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s %s)' % (self.__class__.__name__,
         self.quality_string, self.interval_string)
      
   ## PRIVATE ATTRIBUTES ##

   _acceptable_quality_strings = ('perfect', 'major', 'minor',
      'diminished', 'augmented')

   @property
   def _interval_string(self):
      interval_to_string = {1: 'unison', 2: 'second', 3: 'third', 
         4: 'fourth', 5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'octave',
         9: 'ninth', 10: 'tenth', 11: 'eleventh', 12: 'twelth',
         13: 'thirteenth', 14: 'fourteenth', 15: 'fifteenth'}
      try:
         interval_string = interval_to_string[abs(self.interval_number)]
      except KeyError:
         abs_interval_number = abs(self.interval_number)
         residue = abs_interval_number % 10
         if residue == 1:
            suffix = 'st'
         elif residue == 2:
            suffix = 'nd'
         elif residue == 3:
            suffix = 'rd'
         else:
            suffix = 'th'
         interval_string = '%s%s' % (abs_interval_number, suffix)
      return interval_string

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class(self):
      return ((abs(self.interval_number) - 1) % 7) + 1

   @property
   def interval_number(self):
      return self._interval_number

   @property
   def interval_string(self):
      return self._interval_string

   @property
   def quality_string(self):
      return self._quality_string

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
      return self.interval_number
