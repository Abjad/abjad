from abjad.tools.pitchtools._IntervalClass import _IntervalClass


class _MelodicIntervalClass(_IntervalClass):
   '''.. versionadded:: 1.1.2

   Melodic interval class.
   '''

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return '%s%s' % (self.direction_symbol, abs(self.number))

   ## PUBLIC ATTRIUBTES ##

   @property
   def direction_number(self):
      number = self.number
      if number < 0:
         return -1
      elif number == 0:
         return 0
      else:
         return 1

   @property
   def direction_symbol(self):
      number = self.number
      if number < 0:
         return '-'
      elif number == 0:
         return ''
      else:
         return '+'

   @property
   def direction_word(self):
      number = self.number
      if number < 0:
         return 'descending'
      elif number == 0:
         return ''
      else:
         return 'ascending'
