from abjad.tools.pitchtools import Accidental
import re


class ScaleDegree(object):
   '''.. versionadded:: 1.1.2

   Abjad model of diatonic scale degrees 1, 2, 3, 4, 5, 6, 7 and
   also chromatic alterations including flat-2, flat-3, flat-6, etc.
   '''

   def __init__(self, *args):
      if len(args) == 1 and isinstance(args[0], type(self)):
         self._init_by_scale_degree(*args)
      elif len(args) == 1 and args[0] in self._acceptable_numbers:
         self._init_by_number(*args)
      elif len(args) == 1 and isinstance(args[0], tuple):
         self._init_by_pair(*args)
      elif len(args) == 1 and isinstance(args[0], str):
         self._init_by_symbolic_string(*args)
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

   _roman_numeral_string_to_scale_degree_number = {
      'I': 1,  'II': 2, 'III': 3,
      'IV': 4, 'V': 5,  'VI': 6, 'VII': 7,
   }

   _scale_degree_number_to_roman_numeral_string = {
      1: 'I',  2: 'II', 3: 'III',
      4: 'IV', 5: 'V',  6: 'VI', 7: 'VII',
   }

   _scale_degree_number_to_scale_degree_name = {
      1: 'tonic', 2: 'superdominant', 3: 'mediant',
      4: 'subdominant', 5: 'dominant', 6: 'submediant', 7: 'leading tone',
   }

   _symbolic_string_regex = re.compile(r'([#|b]*)([i|I|v|V]+)')

   ## PRIVATE METHODS ##

   def _init_by_accidental_and_number(self, accidental, number):
      accidental = Accidental(accidental)
      self._accidental = accidental
      self._number = number   

   def _init_by_number(self, number):
      self._number = number
      self._accidental = Accidental(None)
   
   def _init_by_pair(self, pair):
      accidental, number = pair
      self._init_by_accidental_and_number(accidental, number)

   def _init_by_scale_degree(self, scale_degree):
      accidental = scale_degree.accidental
      number = scale_degree.number
      self._init_by_accidental_and_number(accidental, number)

   def _init_by_symbolic_string(self, symbolic_string):
      groups = self._symbolic_string_regex.match(symbolic_string).groups( )
      accidental, roman_numeral = groups
      accidental = Accidental(accidental)
      self._accidental = accidental
      roman_numeral = roman_numeral.upper( )
      number = self._roman_numeral_string_to_scale_degree_number[roman_numeral]
      self._number = number

   ## PUBLIC ATTRIBUTES ##

   @property
   def accidental(self):
      '''Read-only accidental applied to scale degree.'''
      return self._accidental

   @property
   def name(self):
      '''Read-only name of scale degree.'''
      if not self.accidental.is_adjusted:
         return self._scale_degree_number_to_scale_degree_name[self.number]
      else:
         raise NotImplementedError

   @property
   def number(self):
      '''Read-only number of diatonic scale degree from 1 to 7, inclusive.'''
      return self._number

   @property
   def roman_numeral_string(self):
      string = self._scale_degree_number_to_roman_numeral_string[self.number]
      return string

   @property
   def symbolic_string(self):
      return '%s%s' % (self.accidental.symbolic_string, 
         self.roman_numeral_string)

   ## PUBLIC METHODS ##

   def apply_accidental(self, accidental):
      '''Apply accidental to self and emit new instance.'''
      accidental = Accidental(accidental)
      new_accidental = self.accidental + accidental
      return type(self)(new_accidental, self.number)
