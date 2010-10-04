from abjad.tools.pitchtools._DiatonicPitch import _DiatonicPitch


class NumericDiatonicPitch(_DiatonicPitch):
   '''.. versionadded:: 1.1.2

   The Abjad model of a numeric diatonic pitch::

      abjad> pitchtools.NumericDiatonicPitch(7)
      NumericDiatonicPitch(7)
   '''

   __slots__ = ('_diatonic_pitch_number', '_diatonic_pitch_class_number')

   def __new__(klass, arg):
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      if isinstance(arg, (int, long)):
         diatonic_pitch_number = arg
      elif isinstance(arg, str):
         assert pitchtools.is_diatonic_pitch_name_string_with_octave_ticks(arg)
         diatonic_pitch_class_name = arg[0]
         octave_tick_string = arg[1:]
         diatonic_pitch_class_number = \
            self._diatonic_pitch_class_name_string_to_diatonic_pitch_class_number[
            diatonic_pitch_class_name]
         octave_number = pitchtools.octave_tick_string_to_octave_number(octave_tick_string)
         diatonic_pitch_number = 7 * (octave_number - 4) + diatonic_pitch_class_number
      diatonic_pitch_class_number = diatonic_pitch_number % 7
      object.__setattr__(self, '_diatonic_pitch_number', diatonic_pitch_number)
      object.__setattr__(self, '_diatonic_pitch_class_number', diatonic_pitch_class_number)
      return self

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._diatonic_pitch_number)
      
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
      return pitchtools.NumericDiatonicPitchClass(self._diatonic_pitch_class_number)
