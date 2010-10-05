from abjad.tools.pitchtools._DiatonicPitchClass import _DiatonicPitchClass


class NamedDiatonicPitchClass(_DiatonicPitchClass):
   '''.. versionadded:: 1.1.2

   Abjad model of named diatonic pitch class::

      abjad> pitchtools.NamedDiatonicPitchClass('c')
      NamedDiatonicPitchClass('c')
   '''

   __slots__ = ('_diatonic_pitch_class_name_string', )

   def __new__(klass, arg):
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      if isinstance(arg, str):
         assert pitchtools.is_diatonic_pitch_class_name(arg)
         _diatonic_pitch_class_name_string = arg
      elif isinstance(arg, (int, long)):
         _diatonic_pitch_class_number = arg % 7
         _diatonic_pitch_class_name_string = \
            self._diatonic_pitch_class_number_to_diatonic_pitch_class_name_string[
            _diatonic_pitch_class_number]
      else:
         raise TypeError('\n\tMust be int or str: "%s".' % arg)
      object.__setattr__(self, '_diatonic_pitch_class_name_string', 
         _diatonic_pitch_class_name_string)
      return self

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, repr(self.diatonic_pitch_class_name_string))

   ## PUBLIC ATTRIBUTES ##

   @property
   def diatonic_pitch_class_name_string(self):
      '''Read-only name string of diatonic pitch class:

      ::

         abjad> named_diatonic_pitch_class = pitchtools.NamedDiatonicPitchClass('c')
         abjad> named_diatonic_pitch_class.diatonic_pitch_class_name_string
         'c'
      '''
      return self._diatonic_pitch_class_name_string

   @property
   def numeric_diatonic_pitch_class(self):
      '''Numeric diatonic pitch class from named diatonic pitch class:

      ::

         abjad> named_diatonic_pitch_class = pitchtools.NamedDiatonicPitchClass('c')
         abjad> named_diatonic_pitch_class.numeric_diatonic_pitch_class
         NumericDiatonicPitchClass(0)
      '''
      from abjad.tools.pitchtools.NumericDiatonicPitchClass import NumericDiatonicPitchClass
      return NumericDiatonicPitchClass(self.diatonic_pitch_class_name_string)
