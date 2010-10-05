from abjad.tools.pitchtools._DiatonicPitchClass import _DiatonicPitchClass


class NumericDiatonicPitchClass(_DiatonicPitchClass):
   '''.. versionadded:: 1.1.2

   Abjad model of numeric diatonic pitch class::

      abjad> pitchtools.NumericDiatonicPitchClass(0)
      NumericDiatonicPitchClass(0)
   '''

   __slots__ = ('_diatonic_pitch_class_number', )

   def __new__(klass, arg):
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      if isinstance(arg, str):
         assert pitchtools.is_diatonic_pitch_class_name(arg)
         _diatonic_pitch_class_name_string = arg
         _diatonic_pitch_class_number = \
            self._diatonic_pitch_class_name_string_to_diatonic_pitch_class_number[
            _diatonic_pitch_class_name_string]
      elif isinstance(arg, (int, long)):
         _diatonic_pitch_class_number = arg % 7
      else:
         raise TypeError('\n\tMust be int or str: "%s".' % arg)
      object.__setattr__(self, '_diatonic_pitch_class_number', _diatonic_pitch_class_number)
      return self

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, repr(self._diatonic_pitch_class_number))

   ## PUBLIC ATTRIBUTES ##

#   @property
#   def diatonic_pitch_class_number(self):
#      '''Read-only number of diatonic pitch class:
#
#      ::
#
#         abjad> numeric_diatonic_pitch_class = pitchtools.NumericDiatonicPitchClass(0)
#         abjad> numeric_diatonic_pitch_class.diatonic_pitch_class_number
#         0
#      '''
#      return self._diatonic_pitch_class_number

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
