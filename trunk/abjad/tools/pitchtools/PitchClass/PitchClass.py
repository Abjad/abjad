from abjad.tools.pitchtools.get_pitch import get_pitch


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
      if not isinstance(arg, PitchClass):
         raise TypeError
      new_number = (self.number + arg.number) % 12
      return PitchClass(new_number)
      
   def __eq__(self, arg):
      if not isinstance(arg, PitchClass):
         raise TypeError
      return self.number == arg.number

   def __ge__(self, arg):
      if not isinstance(arg, PitchClass):
         raise TypeError
      return self.number >= arg.number

   def __gt__(self, arg):
      if not isinstance(arg, PitchClass):
         raise TypeError
      return self.number > arg.number

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

   def __sub__(self, arg):
      if not isinstance(arg, PitchClass):
         raise TypeError
      new_number = (self.number - arg.number) % 12
      return PitchClass(new_number)
      
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
