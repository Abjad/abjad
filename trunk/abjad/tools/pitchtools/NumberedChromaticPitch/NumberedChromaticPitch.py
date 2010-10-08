from abjad.tools.pitchtools._Pitch import _Pitch
from abjad.tools.pitchtools.Accidental import Accidental



class NumberedChromaticPitch(_Pitch):
   '''.. versionadded:: 1.1.2

   Numeric pitch with middle C defined equal to 0.
   
   Numeric pitches are value objects and can not be changed after creation.
   '''

   def __new__(klass, arg):
      self = object.__new__(klass)
      if isinstance(arg, (int, float, long)):
         #self._number = arg
         number = arg
      elif isinstance(arg, NumberedChromaticPitch):
         #self._number = arg.number
         number = arg.number
      else:
         raise TypeError('can not initialize numeric pitch from %s.' % arg)
      object.__setattr__(self, '_number', number)
      return self

   def __getnewargs__(self):
      return (self.number,)

#   def __init__(self, arg):
#      if isinstance(arg, (int, float, long)):
#         #self._number = arg
#         number = arg
#      elif isinstance(arg, NumberedChromaticPitch):
#         #self._number = arg.number
#         number = arg.number
#      else:
#         raise TypeError('can not initialize numeric pitch from %s.' % arg)
#      object.__setattr__(self, '_number', number)

   ## OVERLOADS ##

   def __abs__(self):
      return NumberedChromaticPitch(abs(self.semitones))

   def __add__(self, arg):
      arg = NumberedChromaticPitch(arg)
      semitones = self.semitones + arg.semitones
      return NumberedChromaticPitch(semitones)
      
   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.number == arg.number:
            return True
      return False

   def __ge__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError
      return self.number >= arg.number

   def __gt__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError
      return self.number > arg.number

   def __hash__(self):
      return hash(repr(self))

   def __le__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError
      return self.number <= arg.number

   def __lt__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError
      return self.number < arg.number

   def __ne__(self, arg):
      return not self == arg

   def __neg__(self):
      return NumberedChromaticPitch(-self.semitones)
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.number)

   def __str__(self):
      return '%s' % self.number

   def __sub__(self, arg):
      arg = NumberedChromaticPitch(arg)
      semitones = self.semitones - arg.semitones
      return NumberedChromaticPitch(semitones)
     
   ## PUBLIC ATTRIBUTES ##

   @property
   def number(self):
      '''Read-only numeric value of numeric pitch.'''
      return self._number

   @property
   def semitones(self):
      '''Read-only number of semitones.'''
      return self.number

   ## PUBLIC METHODS ##

   def apply_accidental(self, accidental = None):
      '''Emit new numeric pitch as sum of self and accidental.'''
      accidental = Accidental(accidental)
      semitones = self.semitones + accidental.semitones
      return type(self)(semitones)

   def transpose(self, n = 0):
      '''Transpose numeric pitch by n.'''
      semitones = self.semitones + n
      return type(self)(semitones)
