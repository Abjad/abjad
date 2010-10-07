from abjad.core import _UnaryComparator


class NamedDiatonicPitch(_UnaryComparator):
   '''.. versionadded:: 1.1.2

   Abjad model of named diatonic pitch::

      abjad> pitchtools.NamedDiatonicPitch("c''")
      NamedDiatonicPitch("c''")
   '''

   __slots__ = ('_diatonic_pitch_name', )

   def __new__(klass, arg):
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      if hasattr(arg, '_diatonic_pitch_name'):
         diatonic_pitch_name = arg._diatonic_pitch_name
      elif hasattr(arg, '_diatonic_pitch_number'):
         tmp = pitchtools.diatonic_pitch_number_to_diatonic_pitch_name
         diatonic_pitch_name = tmp(arg._diatonic_pitch_number)
      elif pitchtools.is_diatonic_pitch_name(arg):
         diatonic_pitch_name = arg
      elif pitchtools.is_diatonic_pitch_number(arg):
         diatonic_pitch_name = pitchtools.diatonic_pitch_number_to_diatonic_pitch_name(arg)
      else:
         raise TypeError('\n\tCan not initialize named diatonic pitch: "%s".' % arg)
      tmp = pitchtools.diatonic_pitch_name_to_diatonic_pitch_number
      diatonic_pitch_number = tmp(diatonic_pitch_name)
      object.__setattr__(self, '_diatonic_pitch_name', diatonic_pitch_name)
      object.__setattr__(self, '_comparison_attribute', diatonic_pitch_number)
      object.__setattr__(self, '_format_string', repr(diatonic_pitch_name))
      return self

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, repr(self._diatonic_pitch_name))

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''Read-only LilyPond input format of named diatonic pitch:

      ::

         abjad> named_diatonic_pitch = pitchtools.NamedDiatonicPitch("c''")
         abjad> named_diatonic_pitch.format
         "c''"
      '''
      return self._diatonic_pitch_name

   @property
   def named_diatonic_pitch_class(self):
      '''Named diatonic pitch-class from named diatonic pitch:

      ::

         abjad> named_diatonic_pitch = pitchtools.NamedDiatonicPitch("c''")
         abjad> named_diatonic_pitch.named_diatonic_pitch_class
         NamedDiatonicPitchClass('c')
      '''
      from abjad.tools import pitchtools
      tmp = pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_name
      return pitchtools.NamedDiatonicPitchClass(tmp(self._diatonic_pitch_name))

   @property
   def numeric_diatonic_pitch(self):
      '''Numeric diatonic pitch from named diatonic pitch:

      ::

         abjad> named_diatonic_pitch = pitchtools.NamedDiatonicPitch("c''")
         abjad> named_diatonic_pitch.numeric_diatonic_pitch
         NumericDiatonicPitch(7)
      '''
      from abjad.tools import pitchtools
      tmp = pitchtools.diatonic_pitch_name_to_diatonic_pitch_number
      return pitchtools.NumericDiatonicPitch(tmp(self._diatonic_pitch_name))

   @property
   def numeric_diatonic_pitch_class(self):
      '''Numeric diatonic pitch class from named diatonic pitch class:

      ::

         abjad> named_diatonic_pitch_class = pitchtools.NamedDiatonicPitch("c''")
         abjad> named_diatonic_pitch.numeric_diatonic_pitch_class
         NumericDiatonicPitchClass(0)
      '''
      from abjad.tools import pitchtools
      tmp = pitchtools.diatonic_pitch_name_to_diatonic_pitch_class_number
      return pitchtools.NumericDiatonicPitchClass(tmp(self._diatonic_pitch_name))
