from abjad.tools.pitchtools._DiatonicPitch import _DiatonicPitch
from abjad.tools.pitchtools._NumericPitch import _NumericPitch


class NumericDiatonicPitch(_DiatonicPitch, _NumericPitch):
   '''.. versionadded:: 1.1.2

   The Abjad model of a numeric diatonic pitch::

      abjad> pitchtools.NumericDiatonicPitch(7)
      NumericDiatonicPitch(7)
   '''

   __slots__ = ('_diatonic_pitch_number', '_diatonic_pitch_class_number')

   def __new__(klass, arg):
      from abjad.tools import mathtools
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      if hasattr(arg, '_diatonic_pitch_number'):
         diatonic_pitch_number = arg._diatonic_pitch_number
      elif mathtools.is_integer_equivalent_number(arg):
         diatonic_pitch_number = arg
      elif pitchtools.is_diatonic_pitch_name(arg):
         diatonic_pitch_number = pitchtools.diatonic_pitch_name_to_diatonic_pitch_number(arg)
      else:
         raise TypeError
      object.__setattr__(self, '_diatonic_pitch_number', diatonic_pitch_number)
      object.__setattr__(self, '_comparison_attribute', diatonic_pitch_number)
      return self

   ## PUBLIC ATTRIBUTES ##

   @property
   def numeric_diatonic_pitch_class(self):
      '''Numeric diatonic pitch-class from numeric diatonic pitch:

      ::

         abjad> numeric_diatonic_pitch = pitchtools.NumericDiatonicPitch(7)
         abjad> numeric_diatonic_pitch.numeric_diatonic_pitch_class
         NumericDiatonicPitchClass(0)
      '''
      from abjad.tools import pitchtools
      tmp = pitchtools.diatonic_pitch_number_to_diatonic_pitch_class_number
      diatonic_pitch_class_number = tmp(self._diatonic_pitch_number)
      return pitchtools.NumericDiatonicPitchClass(diatonic_pitch_class_number)
