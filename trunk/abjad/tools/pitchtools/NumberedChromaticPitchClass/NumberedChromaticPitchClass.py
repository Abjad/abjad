from abjad.tools.pitchtools._PitchClass import _PitchClass
from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClass import \
   InversionEquivalentChromaticIntervalClass
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import \
   get_named_chromatic_pitch_from_pitch_carrier


class NumberedChromaticPitchClass(_PitchClass):
   '''.. versionadded:: 1.1.2

   Numeric 12-ET pitch-class ranging from [0, 12).

   Initialization works with pitch numbers, pitch instances,
   other pitch class instances, notes, and one-note chords.
   '''

   __slots__ = ('_chromatic_pitch_number', )

   ## TODO: use __new__ ##
   
   def __init__(self, arg):
      from abjad.tools import pitchtools
      from abjad.tools.pitchtools.NamedChromaticPitch import NamedChromaticPitch
      from abjad.tools.pitchtools.NamedChromaticPitchClass import NamedChromaticPitchClass
      #if isinstance(arg, (int, long, float)):
      if pitchtools.is_chromatic_pitch_number(arg):
         number = \
            pitchtools.chromatic_pitch_number_to_chromatic_pitch_class_number(arg)
      elif isinstance(arg, type(self)):
         number = arg.number
      elif pitchtools.is_chromatic_pitch_name(arg):
         number = pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number(arg)
      elif isinstance(arg, NamedChromaticPitch):
         #number = arg.pitch_number % 12
         number = arg.numbered_chromatic_pitch._chromatic_pitch_number % 12
      elif isinstance(arg, NamedChromaticPitchClass):
         number = arg.numbered_chromatic_pitch_class.number
      else:
         pitch = get_named_chromatic_pitch_from_pitch_carrier(arg)
         number = pitch.numbered_chromatic_pitch._chromatic_pitch_number % 12
      object.__setattr__(self, '_number', number)

   ## OVERLOADS ##

   def __abs__(self):
      return NumberedChromaticPitchClass(abs(self.semitones))

   def __add__(self, arg):
      '''Addition defined against melodic chromatic intervals only.'''
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('must be melodic chromatic interval.')
      return NumberedChromaticPitchClass(self.number + arg.number % 12)
      
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
      return NumberedChromaticPitchClass(-self.semitones)
   
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
         return InversionEquivalentChromaticIntervalClass(interval_class_number)
      elif isinstance(arg, InversionEquivalentChromaticIntervalClass):
         return NumberedChromaticPitchClass(self.number - arg.number % 12)
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
      return NumberedChromaticPitchClass(semitones)

   def invert(self):
      '''Invert pitch class.'''
      return NumberedChromaticPitchClass(12 - self.number)

   def multiply(self, n):
      '''Multiply pitch class by n.'''
      return NumberedChromaticPitchClass(self.number * n)

   def transpose(self, n):
      '''Transpose pitch class by n.'''
      return NumberedChromaticPitchClass(self.number + n)
