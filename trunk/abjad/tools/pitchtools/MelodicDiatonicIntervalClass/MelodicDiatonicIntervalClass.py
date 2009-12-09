from abjad.tools import mathtools
from abjad.tools.pitchtools._DiatonicIntervalClass import \
   _DiatonicIntervalClass
from abjad.tools.pitchtools._MelodicIntervalClass import \
   _MelodicIntervalClass


class MelodicDiatonicIntervalClass(_DiatonicIntervalClass,
   _MelodicIntervalClass):
   '''.. versionadded:: 1.1.2

   Melodic diatonic interval class.
   '''

   def __init__(self, quality_string, number):
      if quality_string not in self._acceptable_quality_strings:
         raise ValueError('not acceptable quality string.')
      self._quality_string = quality_string
      if not isinstance(number, int):
         raise TypeError('must be integer.')
      if number == 0:
         raise ValueError('must be nonzero.')
      sign = mathtools.sign(number)
      abs_number = abs(number)
      if abs_number % 7 == 1 and 8 <= abs_number:
         number = 8
      else:
         number = abs_number % 7
      if not number == 1:
         number *= sign
      self._number = number

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, MelodicDiatonicIntervalClass):
         if self.direction_number == arg.direction_number:
            if self._quality_string == arg._quality_string:
               if self.number == arg.number:
                  return True
      return False

   def __hash__(self):
      return hash(repr(self))

   def __ne__(self, arg):
      return not self == arg

   def __str__(self):
      return '%s%s%s' % (self.direction_symbol,
         self._quality_abbreviation, abs(self.number))

   ## PRIVATE ATTRIBUTES ##

   @property
   def _full_name(self):
      strings = [ ]
      if self.direction_word:
         strings.append(self.direction_word)
      strings.extend([self._quality_string, self._interval_string])
      return ' '.join(strings)

   ## PUBLIC ATTRIBUTES ##

   @property
   def direction_number(self):
      if self.number < 1:
         return -1
      elif self.number == 1:
         return 0
      else:
         return 1

   @property
   def direction_symbol(self):
      if self.number < 1:
         return '-'
      elif self.number == 1:
         return ''
      else:
         return '+'

   @property
   def direction_word(self):
      if self.number < 1:
         return 'descending'
      elif self.number == 1:
         return ''
      else:
         return 'ascending'
