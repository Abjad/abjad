from abjad.tools.pitchtools.get_pitch import get_pitch
from abjad.tools.pitchtools.IntervalClass import IntervalClass
from abjad.tools.pitchtools.MelodicChromaticInterval import \
   MelodicChromaticInterval


class PitchClass(object):
   '''.. versionadded:: 1.1.2

   12-ET pitch-class ranging from [0, 12).

   Initialization works with pitch numbers, pitch instances,
   other pitch class instances, notes, and one-note chords.
   '''

   def __init__(self, arg):
      from abjad.pitch import Pitch
      if isinstance(arg, (int, long, float)):
         self._number = arg % 12
      elif isinstance(arg, PitchClass):
         self._number = arg.number
      elif isinstance(arg, Pitch):
         self._number = arg.number % 12
      else:
         pitch = get_pitch(arg)
         self._number = pitch.number % 12

   ## OVERLOADS ##

   def __add__(self, arg):
      '''Addition defined against melodic chromatic intervals only.'''
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('must be melodic chromatic interval.')
      return PitchClass(self.number + arg.number % 12)
      
   def __eq__(self, arg):
      if isinstance(arg, PitchClass):
         return self.number == arg.number
      return False

   def __ge__(self, arg):
      if not isinstance(arg, PitchClass):
         raise TypeError
      return self.number >= arg.number

   def __gt__(self, arg):
      if not isinstance(arg, PitchClass):
         raise TypeError
      return self.number > arg.number

   def __hash__(self):
      return hash(repr(self))

   def __le__(self, arg):
      if not isinstance(arg, PitchClass):
         raise TypeError
      return self.number <= arg.number

   def __lt__(self, arg):
      if not isinstance(arg, PitchClass):
         raise TypeError
      return self.number < arg.number

   def __ne__(self, arg):
      return not self == arg
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.number)

   def __str__(self):
      return '%s' % self.number

   def __sub__(self, arg):
      '''Subtraction defined against both melodic chromatic intevals
      and against other pitch classes.'''
      if isinstance(arg, PitchClass):
         interval_class_number = abs(self.number - arg.number)
         if 6 < interval_class_number:
            interval_class_number = 12 - interval_class_number
         return IntervalClass(interval_class_number)
      elif isinstance(arg, IntervalClass):
         return PitchClass(self.number - arg.number % 12)
      else:
         raise TypeError('must be pitch class or interval class.')
     
   ## PUBLIC ATTRIBUTES ##

   @property
   def number(self):
      '''Read-only numeric value of pitch-class.'''
      return self._number

   ## PUBLIC METHODS ##

   def invert(self):
      '''Invert pitch class.'''
      return PitchClass(12 - self.number)

   def multiply(self, n):
      '''Multiply pitch class by n.'''
      return PitchClass(self.number * n)

   def transpose(self, n):
      '''Transpose pitch class by n.'''
      return PitchClass(self.number + n)
