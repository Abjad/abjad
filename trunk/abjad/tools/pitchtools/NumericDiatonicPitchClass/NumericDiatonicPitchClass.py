from abjad.tools.pitchtools._DiatonicPitchClass import _DiatonicPitchClass
from abjad.tools.pitchtools._NumericPitchClass import _NumericPitchClass


class NumericDiatonicPitchClass(_NumericPitchClass, _DiatonicPitchClass):
   '''.. versionadded:: 1.1.2

   Abjad model of a numeric diatonic pitch class::

      abjad> pitchtools.NumericDiatonicPitchClass(0)
      NumericDiatonicPitchClass(0)
   '''

   __slots__ = ('_diatonic_pitch_class_number', )

   def __new__(klass, arg):
      from abjad.tools import mathtools
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      if hasattr(arg, '_diatonic_pitch_class_number'):
         diatonic_pitch_class_number = arg._diatonic_pitch_class_number
      elif isinstance(arg, str):
         if not pitchtools.is_diatonic_pitch_class_name(arg):
            raise ValueError
         diatonic_pitch_class_name = arg
         tmp = pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number
         diatonic_pitch_class_number = tmp(diatonic_pitch_class_name)
      elif mathtools.is_integer_equivalent_number(arg):
         diatonic_pitch_class_number = int(arg) % 7
      else:
         raise TypeError
      object.__setattr__(self, '_diatonic_pitch_class_number', diatonic_pitch_class_number)
      object.__setattr__(self, '_comparison_attribute', diatonic_pitch_class_number)
      object.__setattr__(self, '_format_string', diatonic_pitch_class_number)
      return self

   @property
   def named_diatonic_pitch_class(self):
      '''Named diatonic pitch class from numeric diatonic pitch class:

      ::

         abjad> numeric_diatonic_pitch_class = pitchtools.NumericDiatonicPitchClass(0)
         abjad> numeric_diatonic_pitch_class.named_diatonic_pitch_class
         NamedDiatonicPitchClass('c')
      '''
      from abjad.tools.pitchtools.NamedDiatonicPitchClass import NamedDiatonicPitchClass
      return NamedDiatonicPitchClass(self.diatonic_pitch_class_number)
