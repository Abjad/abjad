from abjad.tools.pitchtools._DiatonicPitchClass import _DiatonicPitchClass
from abjad.tools.pitchtools._NumberedPitchClass import _NumberedPitchClass


class NumberedDiatonicPitchClass(_NumberedPitchClass, _DiatonicPitchClass):
   '''.. versionadded:: 1.1.2

   Abjad model of a numeric diatonic pitch class::

      abjad> pitchtools.NumberedDiatonicPitchClass(0)
      NumberedDiatonicPitchClass(0)
   '''

   __slots__ = ('_diatonic_pitch_class_number', )

   def __new__(klass, arg):
      from abjad.tools import mathtools
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      if hasattr(arg, '_diatonic_pitch_class_number'):
         diatonic_pitch_class_number = arg._diatonic_pitch_class_number
      elif pitchtools.is_chromatic_pitch_name(arg):
         tmp = pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_number
         diatonic_pitch_class_number = tmp(arg)
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

         abjad> numbered_diatonic_pitch_class = pitchtools.NumberedDiatonicPitchClass(0)
         abjad> numbered_diatonic_pitch_class.named_diatonic_pitch_class
         NamedDiatonicPitchClass('c')
      '''
      from abjad.tools.pitchtools.NamedDiatonicPitchClass import NamedDiatonicPitchClass
      return NamedDiatonicPitchClass(self.diatonic_pitch_class_number)
