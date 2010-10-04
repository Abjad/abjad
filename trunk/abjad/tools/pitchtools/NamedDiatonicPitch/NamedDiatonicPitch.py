from abjad.tools.pitchtools._DiatonicPitch import _DiatonicPitch


class NamedDiatonicPitch(_DiatonicPitch):
   '''.. versionadded:: 1.1.2

   Abjad model of named diatonic pitch::

      abjad> pitchtools.NamedDiatonicPitch("c''")
      NamedDiatonicPitch("c''")
   '''

   __slots__ = ('_diatonic_pitch_class_name', '_diatonic_pitch_class_number', 
      '_octave_number', '_tick_string')

   def __new__(klass, arg):
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      if hasattr(arg, 'diatonic_pitch_class'):
         diatonic_pitch_class_name = arg.diatonic_pitch_class.name
         diatonic_pitch_class_number = arg.diatonic_pitch_class.number
         octave_number = arg.octave_number
         tick_string = pitchtools.octave_number_to_octave_tick_string(octave_number)
      elif isinstance(arg, str):
         assert pitchtools.is_diatonic_pitch_name_string_with_octave_ticks(arg)
         diatonic_pitch_class_name = arg[0]
         diatonic_pitch_class_number = \
            self._diatonic_pitch_class_name_string_to_diatonic_pitch_class_number[
            diatonic_pitch_class_name]
         tick_string = arg[1:]
         octave_number = pitchtools.octave_tick_string_to_octave_number(tick_string)
         diatonic_pitch_number = 7 * (octave_number - 4) + diatonic_pitch_class_number
      elif isinstance(arg, (int, long)):
         diatonic_pitch_number = arg
         diatonic_pitch_class_number = arg % 7
         diatonic_pitch_class_name = \
            self._diatonic_pitch_class_number_to_diatonic_pitch_class_name_string[
            diatonic_pitch_class_number]
         octave_number = arg // 7 + 4
         tick_string = pitchtools.octave_number_to_octave_tick_string(octave_number)
      else:
         raise TypeError('\n\tCan not initialize named diatonic pitch: "%s".' % arg)
      object.__setattr__(self, '_diatonic_pitch_class_name', 
         diatonic_pitch_class_name)
      object.__setattr__(self, '_octave_number', octave_number)
      object.__setattr__(self, '_tick_string', tick_string)
      diatonic_pitch_name = diatonic_pitch_class_name + tick_string
      object.__setattr__(self, '_diatonic_pitch_name', diatonic_pitch_name)
      object.__setattr__(self, '_diatonic_pitch_number', diatonic_pitch_number)
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
      return pitchtools.NamedDiatonicPitchClass(self._diatonic_pitch_class_name)

   @property
   def numeric_diatonic_pitch(self):
      '''Numeric diatonic pitch from named diatonic pitch:

      ::

         abjad> named_diatonic_pitch = pitchtools.NamedDiatonicPitch("c''")
         abjad> named_diatonic_pitch.numeric_diatonic_pitch
         NumericDiatonicPitch(7)
      '''
      from abjad.tools import pitchtools
      return pitchtools.NumericDiatonicPitch(self._diatonic_pitch_number)

   @property
   def numeric_diatonic_pitch_class(self):
      '''Numeric diatonic pitch class from named diatonic pitch class:

      ::

         abjad> named_diatonic_pitch_class = pitchtools.NamedDiatonicPitch("c''")
         abjad> named_diatonic_pitch.numeric_diatonic_pitch_class
         NumericDiatonicPitchClass(0)
      '''
      from abjad.tools import pitchtools
      return pitchtools.NumericDiatonicPitchClass(self._diatonic_pitch_class_name)
