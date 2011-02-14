from abjad.tools.pitchtools._PitchClass import _PitchClass
from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClass import \
   InversionEquivalentChromaticIntervalClass
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import \
   get_named_chromatic_pitch_from_pitch_carrier


class NumberedChromaticPitchClass(_PitchClass):
   '''.. versionadded:: 1.1.2

   The Abjad model of a numbered chromatic pitch-class::

      abjad> pitchtools.NumberedChromaticPitchClass(13)
      NumberedChromaticPitchClass(1)

   Numbered chromatic pitch-classes are immutable.
   '''

   __slots__ = ('_chromatic_pitch_class_number', )

   ## TODO: use __new__ ##
   
   def __init__(self, arg):
      from abjad.tools import pitchtools
      from abjad.tools.pitchtools.NamedChromaticPitch import NamedChromaticPitch
      from abjad.tools.pitchtools.NamedChromaticPitchClass import NamedChromaticPitchClass
      if pitchtools.is_chromatic_pitch_number(arg):
         number = \
            pitchtools.chromatic_pitch_number_to_chromatic_pitch_class_number(arg)
      elif isinstance(arg, type(self)):
         number = abs(arg)
      elif pitchtools.is_chromatic_pitch_name(arg):
         number = pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_number(arg)
      elif isinstance(arg, NamedChromaticPitch):
         number = abs(arg.numbered_chromatic_pitch) % 12
      elif isinstance(arg, NamedChromaticPitchClass):
         number = abs(arg.numbered_chromatic_pitch_class)
      else:
         pitch = get_named_chromatic_pitch_from_pitch_carrier(arg)
         number = abs(pitch.numbered_chromatic_pitch) % 12
      object.__setattr__(self, '_chromatic_pitch_class_number', number)
      object.__setattr__(self, '_comparison_attribute', number)

   ## OVERLOADS ##

   def __abs__(self):
      return self._chromatic_pitch_class_number

   def __add__(self, arg):
      '''Addition defined against melodic chromatic intervals only.'''
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('must be melodic chromatic interval.')
      return NumberedChromaticPitchClass(abs(self) + arg.number % 12)

   def __float__(self):
      return float(self._chromatic_pitch_class_number)

   def __int__(self):
      return self._chromatic_pitch_class_number
      
   def __neg__(self):
      return NumberedChromaticPitchClass(-abs(self))
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, abs(self))

   def __str__(self):
      return str(abs(self))

   def __sub__(self, arg):
      '''Subtraction defined against both melodic chromatic intervals
      and against other pitch classes.'''
      if isinstance(arg, type(self)):
         interval_class_number = abs(abs(self) - abs(arg))
         if 6 < interval_class_number:
            interval_class_number = 12 - interval_class_number
         return InversionEquivalentChromaticIntervalClass(interval_class_number)
      elif isinstance(arg, InversionEquivalentChromaticIntervalClass):
         return NumberedChromaticPitchClass(abs(self) - arg.number % 12)
      else:
         raise TypeError('must be pitch class or interval class.')
     
   ## PUBLIC ATTRIBUTES ##

   ## PUBLIC METHODS ##

   def apply_accidental(self, accidental = None):
      '''Emit new numeric pitch class as sum of self and accidental.'''
      from abjad.tools.pitchtools.Accidental import Accidental
      accidental = Accidental(accidental)
      semitones = abs(self) + accidental.semitones
      return NumberedChromaticPitchClass(semitones)

   def invert(self):
      '''Invert pitch class.'''
      return NumberedChromaticPitchClass(12 - abs(self))

   def multiply(self, n):
      '''Multiply pitch class by n.'''
      return NumberedChromaticPitchClass(abs(self) * n)

   def transpose(self, n):
      '''Transpose pitch class by n.'''
      return NumberedChromaticPitchClass(abs(self) + n)
