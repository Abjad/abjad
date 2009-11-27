from abjad.tools import mathtools


class DiatonicInterval(object):
   '''.. versionadded:: 1.1.2

   Diatonic interval. ::

      abjad> interval = pitchtools.DiatonicInterval('minor', -3)
      abjad> interval
      DiatonicInterval(descending minor third)
   '''

   def __init__(self, quality_string, interval_number):
      if quality_string in self._acceptable_quality_strings:
         self._quality_string = quality_string
      else:
         raise ValueError(
            'quality must be in %s' % self._acceptable_quality_strings)
      if isinstance(interval_number, int):
         if int == 0:
            raise ValueError
         self._interval_number = interval_number
      else:
         raise ValueError('interval must be integer.')

   ## OVERLOADS ##

   def __abs__(self):
      return DiatonicInterval(self.quality_string, abs(self.interval_number))

   def __eq__(self, expr):
      if isinstance(expr, DiatonicInterval):
         if self.quality_string == expr.quality_string:
            if self.interval_number == expr.interval_number:
               return True
      return False

   def __ne__(self, expr):
      return not self == expr

   def __neg__(self):
      return DiatonicInterval(self.quality_string, -self.interval_number)

   def __repr__(self):
      if self.direction_string:
         return '%s(%s %s %s)' % (self.__class__.__name__, 
            self.direction_string, self.quality_string, self.interval_string)
      else:
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
         interval_string = '%sth' % self.interval_number
      return interval_string

   ## PUBLIC ATTRIBUTES ##

   @property
   def counterpoint_interval(self):
      counterpoint_interval = self.interval_class
      if counterpoint_interval == 1:
         if self.interval_number == 1:
            return 1
         else:
            return 8
      return counterpoint_interval

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
      interval_to_semitones = {
         1: 0, 2: 1, 3: 3, 4: 5, 5: 7, 6: 8, 7: 10, 8: 12,
         9: 13, 10: 15, 11: 17, 12: 19, 13: 20, 14: 22, 15: 24}
      result += interval_to_semitones[abs(self.interval_number)]
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
