from abjad.tools.pitchtools._ChromaticPitch import _ChromaticPitch
from abjad.tools.pitchtools._NumberedPitch import _NumberedPitch


class NumberedChromaticPitch(_ChromaticPitch, _NumberedPitch):
   '''.. versionadded:: 1.1.2

   Abjad model of a numbered chromatic pitch::

      abjad> pitchtools.NumberedChromaticPitch(13)
      NumberedChromaticPitch(13)

   Numbered chromatic pitches are immutable.
   '''

   __slots__ = ('_chromatic_pitch_number', )

   def __new__(klass, arg):
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      if hasattr(arg, '_chromatic_pitch_number'):
         chromatic_pitch_number = arg._chromatic_pitch_number
      elif pitchtools.is_chromatic_pitch_number(arg):
         chromatic_pitch_number = arg
      elif pitchtools.is_chromatic_pitch_name(arg):
         chromatic_pitch_number = pitchtools.chromatic_pitch_name_to_chromatic_pitch_number(arg)
      else:
         raise TypeError('can not initialize numbered chromatic pitch from "%s".' % arg)
      object.__setattr__(self, '_chromatic_pitch_number', chromatic_pitch_number)
      object.__setattr__(self, '_comparison_attribute', chromatic_pitch_number)
      return self

   def __getnewargs__(self):
      return (self._chromatic_pitch_number, )

   ## OVERLOADS ##

   def __abs__(self):
      return self._chromatic_pitch_number

   def __add__(self, arg):
      arg = type(self)(arg)
      semitones = abs(self) + abs(arg)
      return type(self)(semitones)

   def __float__(self):
      return float(self._chromatic_pitch_number)
      
   def __hash__(self):
      return hash(repr(self))

   def __int__(self):
      return self._chromatic_pitch_number

   def __neg__(self):
      return type(self)(-abs(self))
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, abs(self))

   def __str__(self):
      return '%s' % abs(self)

   def __sub__(self, arg):
      arg = type(self)(arg)
      semitones = abs(self) - abs(arg)
      return type(self)(semitones)
     
   ## PUBLIC ATTRIBUTES ##

   ## PUBLIC METHODS ##

   def apply_accidental(self, accidental = None):
      '''Emit new numbered chromatic pitch as sum of self and accidental.'''
      from abjad.tools.pitchtools.Accidental import Accidental
      accidental = Accidental(accidental)
      semitones = abs(self) + accidental.semitones
      return type(self)(semitones)

   def transpose(self, n = 0):
      '''Transpose numbered chromatic pitch by n.'''
      semitones = abs(self) + n
      return type(self)(semitones)
