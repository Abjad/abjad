from abjad.tools.pitchtools.get_pitch import get_pitch
from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.IntervalClass import IntervalClass
from abjad.tools.pitchtools.MelodicChromaticInterval import \
   MelodicChromaticInterval


class PitchClass(object):
   '''.. versionadded:: 1.1.2

   Numeric 12-ET pitch-class ranging from [0, 12).

   Initialization works with pitch numbers, pitch instances,
   other pitch class instances, notes, and one-note chords.
   '''

   def __init__(self, arg):
      from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
      from abjad.tools.pitchtools.NamedPitchClass import NamedPitchClass
      if isinstance(arg, (int, long, float)):
         self._number = arg % 12
      elif isinstance(arg, type(self)):
         self._number = arg.number
      elif isinstance(arg, str):
         named_pitch_class = NamedPitchClass(arg)
         self._number = named_pitch_class.numeric_pitch_class.number
      elif isinstance(arg, NamedPitch):
         self._number = arg.number % 12
      elif isinstance(arg, NamedPitchClass):
         self._number = arg.numeric_pitch_class.number
      else:
         pitch = get_pitch(arg)
         self._number = pitch.number % 12

   ## OVERLOADS ##

   def __abs__(self):
      return PitchClass(abs(self.semitones))

   def __add__(self, arg):
      '''Addition defined against melodic chromatic intervals only.'''
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('must be melodic chromatic interval.')
      return PitchClass(self.number + arg.number % 12)
      
   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self.number == arg.number
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
      return PitchClass(-self.semitones)
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.number)

   def __str__(self):
      return '%s' % self.number

   def __sub__(self, arg):
      '''Subtraction defined against both melodic chromatic intervals
      and against other pitch classes.'''
      if isinstance(arg, type(self)):
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

   @property
   def semitones(self):
      '''Read-only number of semitones.'''
      return self.number

   ## PUBLIC METHODS ##

   def apply_accidental(self, accidental = None):
      '''Emit new numeric pitch class as sum of self and accidental.'''
      accidental = Accidental(accidental)
      semitones = self.semitones + accidental.semitones
      return PitchClass(semitones)

   def invert(self):
      '''Invert pitch class.'''
      return PitchClass(12 - self.number)

   def multiply(self, n):
      '''Multiply pitch class by n.'''
      return PitchClass(self.number * n)

   def transpose(self, n):
      '''Transpose pitch class by n.'''
      return PitchClass(self.number + n)
