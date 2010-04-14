from abjad.tools.pitchtools import Accidental


class ScaleDegree(object):
   '''.. versionadded:: 1.1.2

   Abjad model of diatonic scale degrees 1, 2, 3, 4, 5, 6, 7 and
   also chromatic alterations including flat-2, flat-3, flat-6, etc.
   '''

   def __init__(self, number, accidental = None):
      if number not in (1, 2, 3, 4, 5, 6, 7):
         raise ValueError('scale degree %s must be 1 - 7.' % number)
      self._number = number
      accidental = Accidental(accidental)
      self._accidental = accidental

   ## OVERLOADS ##
   
   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.number == arg.number:
            if self.accidental == arg.accidental:
               return True
      return False
      
   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return self._compact_format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _compact_format_string(self):
      return '%s%s' % (self.accidental.symbolic_string, self.number)

   @property
   def _format_string(self):
      parts = [ ]
      parts.append(str(self.number))
      if not self.accidental.string == '':
         parts.append(self.accidental.name)
      return ', '.join(parts)

   ## PUBLIC ATTRIBUTES ##

   @property
   def accidental(self):
      return self._accidental

   @property
   def number(self):
      return self._number
