from abjad.tools.pitchtools import Accidental


class ScaleDegree(object):
   '''.. versionadded:: 1.1.2

   Abjad model of diatonic scale degrees 1, 2, 3, 4, 5, 6, 7 and
   also chromatic alterations including flat-2, flat-3, flat-6, etc.
   '''

   def __init__(self, *args):
      if len(args) == 1 and args[0] in self._acceptable_numbers:
         self._init_by_number(*args)
      elif len(args) == 1 and isinstance(args[0], type(self)):
         self._init_by_number(args[0].number)
      elif len(args) == 2 and args[1] in self._acceptable_numbers:
         self._init_by_accidental_and_number(*args)
      else:
         arg_string = ', '.join([str(x) for x in args])
         raise ValueError('can not initialize scale degree: %s.' % arg_string)

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
   def _acceptable_numbers(self):
      return (1, 2, 3, 4, 5, 6, 7)

   @property
   def _compact_format_string(self):
      return '%s%s' % (self.accidental.symbolic_string, self.number)

   @property
   def _format_string(self):
      parts = [ ]
      if self.accidental.is_adjusted:
         parts.append(self.accidental.name)
      parts.append(str(self.number))
      return ', '.join(parts)

   ## PRIVATE METHODS ##

   def _init_by_accidental_and_number(self, accidental, number):
      accidental = Accidental(accidental)
      self._accidental = accidental
      self._number = number   

   def _init_by_number(self, number):
      self._number = number
      self._accidental = Accidental(None)

   ## PUBLIC ATTRIBUTES ##

   @property
   def accidental(self):
      '''Read-only accidental applied to scale degree.'''
      return self._accidental

   @property
   def number(self):
      '''Read-only number of diatonic scale degree from 1 to 7, inclusive.'''
      return self._number

   ## PUBLIC METHODS ##

   def apply_accidental(self, accidental):
      '''Apply accidental to self and emit new instance.'''
      accidental = Accidental(accidental)
      new_accidental = self.accidental + accidental
      return type(self)(new_accidental, self.number)
