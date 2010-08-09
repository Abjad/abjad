from abjad.tools.pitchtools._CounterpointInterval import _CounterpointInterval
from abjad.tools.pitchtools._MelodicInterval import _MelodicInterval
from abjad.tools.pitchtools.MelodicCounterpointIntervalClass import MelodicCounterpointIntervalClass


class MelodicCounterpointInterval(_CounterpointInterval, _MelodicInterval):
   '''.. versionadded:: 1.1.2

   Melodic counterpoint interval.
   Like a reduced diatonic interval stripped of major, minor
   or other quality. Similar to the numbers of figured bass.
   '''

   def __init__(self, number):
      if not isinstance(number, int):
         raise TypeError('must be integer.')
      if number == 0:
         raise ValueError('must be nonzero integer.')
      if abs(number) == 1:
         number = 1
      self._number = number

   ## OVERLOADS ##
  
   def __str__(self):
      return self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return '%s%s' % (self._direction_symbol, abs(self.number))

   ## PUBLIC ATTRIBUTES ##

   @property
   def direction_number(self):
      if self.number < 0:
         return -1
      elif self.number == 1:
         return 0
      elif 1 < self.number:
         return 1
      else:
         raise ValueError

   @property
   def interval_class(self):
      return MelodicCounterpointIntervalClass(self)
