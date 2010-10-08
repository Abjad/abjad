from abjad.cfg._read_config_file import _read_config_file
from abjad.tools.pitchtools._Pitch import _Pitch


## TODO: remove ##
_accidental_spelling = _read_config_file( )['accidental_spelling']

class NamedChromaticPitch(_Pitch):
   '''Abjad model of named pitch:

   ::

      abjad> pitchtools.NamedChromaticPitch("cs'")
      NamedChromaticPitch("cs'")
   '''

   ## TODO: remove ##
   accidental_spelling = _accidental_spelling

   __slots__ = ('_chromatic_pitch_name', '_deviation')

   def __new__(klass, *args, **kwargs):
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      _deviation = kwargs.get('deviation', None)
      object.__setattr__(self, '_deviation', _deviation)
      if len(args) == 1 and isinstance(args[0], (int, long, float)):
         self._init_by_chromatic_pitch_number(*args)
      elif len(args) == 1 and isinstance(args[0], type(self)):
         self._init_by_named_pitch(*args)
      elif len(args) == 1 and hasattr(args[0], 'named_pitch'):
         self._init_by_named_pitch(args[0].named_pitch)
      elif len(args) == 1 and pitchtools.is_chromatic_pitch_class_name_octave_number_pair(args[0]):
         self._init_by_chromatic_pitch_class_name_octave_number_pair(*args)
      elif len(args) == 1 and isinstance(args[0], str):
         self._init_by_chromatic_pitch_name(*args)
      elif len(args) == 2 and isinstance(args[0], str):
         self._init_by_chromatic_pitch_class_name_and_octave_number(*args)
      elif len(args) == 2 and isinstance(args[0], pitchtools.NamedChromaticPitchClass):
         self._init_by_named_pitch_class_and_octave_number(*args)
      elif len(args) == 2 and isinstance(args[0], (int, long, float)):
         if isinstance(args[1], str):
            self._init_by_chromatic_pitch_number_and_diatonic_pitch_class_name(*args)
         elif isinstance(args[1], pitchtools.NamedChromaticPitchClass):
            self._init_by_chromatic_pitch_number_and_named_pitch_class(*args)
         else:
            raise TypeError
      elif len(args) == 3:
         self._init_by_chromatic_pitch_class_name_octave_number_and_deviation(*args)
      else:
         raise ValueError('\n\tNot a valid pitch token: "%s".' % str(args))
      assert hasattr(self, '_deviation')
      assert hasattr(self, '_chromatic_pitch_name')
      return self

   def __getnewargs__(self):
      #return (self._chromatic_pitch_class_name, self.octave_number)
      return (self._chromatic_pitch_name, self._deviation)

   ## OVERLOADS ##

   def __add__(self, melodic_interval):
      '''.. versionadded:: 1.1.2'''
      from abjad.tools import pitchtools
      return pitchtools.transpose_pitch_carrier_by_melodic_interval(self, melodic_interval)

   def __copy__(self):
      '''.. versionadded:: 1.1.2'''
      return type(self)(self)

   def __eq__(self, arg):
      try:
         arg = type(self)(arg)
         if self._chromatic_pitch_name == arg._chromatic_pitch_name:
            if self.deviation == arg.deviation:
               return True
         return False
      except (TypeError, ValueError):
         return False

   def __ge__(self, arg):
      try:
         arg = type(self)(arg)
         return self._diatonic_pitch_number > arg._diatonic_pitch_number or \
            (self._diatonic_pitch_number == arg._diatonic_pitch_number and
            self.accidental.semitones >= arg.accidental.semitones) or \
            (self._diatonic_pitch_number == arg._diatonic_pitch_number and
            self.accidental == arg.accidental and
            self._numeric_deviation >= arg._numeric_deviation)
      except (TypeError, ValueError):
         return False

   def __gt__(self, arg):
      if not isinstance(arg, type(self)):
         return False
      return self._diatonic_pitch_number > arg._diatonic_pitch_number or \
         (self._diatonic_pitch_number == arg._diatonic_pitch_number and \
         self.accidental.semitones > arg.accidental.semitones) or \
         (self._diatonic_pitch_number == arg._diatonic_pitch_number and \
         self.accidental == arg.accidental and \
         self._numeric_deviation > arg._numeric_deviation)

   def __hash__(self):
      return hash(repr(self))

   def __le__(self, arg):
      if not isinstance(arg, type(self)):
         return False
      if not self._diatonic_pitch_number == arg._diatonic_pitch_number:
         return self._diatonic_pitch_number <= arg._diatonic_pitch_number
      if not self.accidental == arg.accidental:
         return self.accidental <= arg.accidental
      return self._numeric_deviation <= arg._numeric_deviation

   def __lt__(self, arg):
      if not isinstance(arg, type(self)):
         return False
      return self._diatonic_pitch_number < arg._diatonic_pitch_number or \
         (self._diatonic_pitch_number == arg._diatonic_pitch_number and \
         self.accidental.semitones < arg.accidental.semitones) or \
         (self._diatonic_pitch_number == arg._diatonic_pitch_number and \
         self.accidental == arg.accidental and \
         self._numeric_deviation < arg._numeric_deviation)

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      if self._pitch_class_name and not self.octave_number is None:
         if self.deviation is None:
            return '%s(%s)' % (self.__class__.__name__, repr(str(self)))
         else:
            return '%s(%s, deviation = %s)' % (self.__class__.__name__,
               repr(str(self)), self.deviation)
      else:
         return '%s( )' % self.__class__.__name__

   def __str__(self):
      if self._pitch_class_name and not self.octave_number is None:
         return '%s%s' % (self._pitch_class_name, self._octave_tick_string)
      else:
         return ''

   def __sub__(self, arg):
      from abjad.tools import pitchtools
      if isinstance(arg, type(self)):
         return pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
            self, arg)
      else:
         interval = arg
         return pitchtools.transpose_pitch_carrier_by_melodic_interval(self, -interval)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _diatonic_pitch_number(self):
      '''Read-only diatonic pitch number of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch._diatonic_pitch_number
         0
      '''
      if self.diatonic_pitch_class_name:
         return (self.octave_number - 4) * 7 + self.diatonic_pitch_class_number
      else:
         return None

   @property
   def diatonic_pitch_number(self):
      return self._diatonic_pitch_number

   @property
   def _numeric_deviation(self):
      if self.deviation is None:
         return 0
      else:
         return self.deviation

   @property
   def _octave_tick_string(self):
      '''Read-only octave tick string of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch._octave_tick_string
         "'"
      '''
      if self.octave_number is not None:
         if self.octave_number <= 2:
            return ',' * (3 - self.octave_number)
         elif self.octave_number == 3:
            return ''
         else:
            return "'" * (self.octave_number - 3)
      else:
         return None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _pitch_class_name(self):
      '''Read-only pitch-class name of pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.pitch_class_name
         'cs'
      '''
      if self.diatonic_pitch_class_name and self.accidental:
         return '%s%s' % (self.diatonic_pitch_class_name, self.accidental)
      else:
         return None

   ## PRIVATE METHODS ##

   def _init_by_chromatic_pitch_class_name_and_octave_number(
      self, chromatic_pitch_class_name, octave_number):
      from abjad.tools import pitchtools
      octave_tick_string = pitchtools.octave_number_to_octave_tick_string(octave_number)
      chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string
      object.__setattr__(self, '_chromatic_pitch_name', chromatic_pitch_name)
      
   def _init_by_chromatic_pitch_class_name_octave_number_and_deviation(
      self, name, octave, deviation):
      self._init_by_chromatic_pitch_class_name_and_octave_number(name, octave)
      object.__setattr__(self, '_deviation', deviation)

   def _init_by_named_pitch_class_and_octave_number(self, npc, octave_number):
      self._init_by_chromatic_pitch_class_name_and_octave_number(npc.name, octave_number)

   def _init_by_chromatic_pitch_number(self, chromatic_pitch_number):
      from abjad.tools import pitchtools
      accidental_spelling = self.accidental_spelling
      chromatic_pitch_name = pitchtools.chromatic_pitch_number_to_chromatic_pitch_name(
         chromatic_pitch_number, accidental_spelling)
      object.__setattr__(self, '_chromatic_pitch_name', chromatic_pitch_name)

   def _init_by_chromatic_pitch_number_and_diatonic_pitch_class_name(
      self, chromatic_pitch_number, diatonic_pitch_class_name):
      from abjad.tools import pitchtools
      alphabetic_accidental_abbreviation, octave_number = \
         pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_abbreviation_octave_number_pair(
         chromatic_pitch_number, diatonic_pitch_class_name)
      octave_tick_string = pitchtools.octave_number_to_octave_tick_string(octave_number)
      chromatic_pitch_class_name = diatonic_pitch_class_name + alphabetic_accidental_abbreviation
      chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string
      object.__setattr__(self, '_chromatic_pitch_name', chromatic_pitch_name)

   def _init_by_chromatic_pitch_number_and_named_pitch_class(self, pitch_number, npc):
      diatonic_pitch_class_name = npc.name[:1]
      self._init_by_chromatic_pitch_number_and_diatonic_pitch_class_name(
         pitch_number, diatonic_pitch_class_name)

   def _init_by_chromatic_pitch_class_name_octave_number_pair(self, pair):
      from abjad.tools import pitchtools
      chromatic_pitch_class_name, octave_number = pair
      octave_tick_string = pitchtools.octave_number_to_octave_tick_string(octave_number)
      chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string
      object.__setattr__(self, '_chromatic_pitch_name', chromatic_pitch_name)

   def _init_by_chromatic_pitch_name(self, pitch_string):
      from abjad.tools import pitchtools
      name = pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name(pitch_string)
      octave_number = pitchtools.chromatic_pitch_name_to_octave_number(pitch_string)
      self._init_by_chromatic_pitch_class_name_and_octave_number(name, octave_number)

   def _init_by_named_pitch(self, named_pitch):
      from abjad.tools import pitchtools
      object.__setattr__(self, '_chromatic_pitch_name', named_pitch._chromatic_pitch_name)
      object.__setattr__(self, '_deviation', named_pitch.deviation)

   ## PUBLIC ATTRIBUTES ##

   @property
   def accidental(self):
      '''Read-only accidental of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.accidental
         Accidental('s')
      '''
      #return self._accidental
      from abjad.tools.pitchtools.Accidental import Accidental
      from abjad.tools.pitchtools.is_chromatic_pitch_name import chromatic_pitch_name_regex
      groups = chromatic_pitch_name_regex.match(self._chromatic_pitch_name).groups( )
      alphabetic_accidental_abbreviation = groups[1]
      return Accidental(alphabetic_accidental_abbreviation)

   @property
   def deviation(self):
      '''Read-only deviation of named pitch in cents:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.deviation is None
         True
      '''
      return self._deviation


   @property
   def diatonic_pitch_class_number(self):
      '''Read-only diatonic pitch-class number of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.diatonic_pitch_class_number
         0
      '''
      from abjad.tools import pitchtools
      return pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number(
         self.diatonic_pitch_class_name)

   @property
   def format(self):
      '''Read-only LilyPond input format of pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.format
         "cs'"
      '''
      return str(self)

   @property
   def diatonic_pitch_class_name(self):
      '''Read-only diatonic pitch-class name of pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.diatonic_pitch_class_name
         'c'
      '''
      from abjad.tools import pitchtools
      return pitchtools.chromatic_pitch_name_to_diatonic_pitch_class_name(
         self._chromatic_pitch_name)

   @property
   def named_diatonic_pitch(self):
      '''Named diatonic pitch from named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs''")
         abjad> named_pitch.named_diatonic_pitch
         NamedDiatonicPitch("c''")
      '''
      from abjad.tools import pitchtools
      tmp = pitchtools.chromatic_pitch_name_to_diatonic_pitch_name
      diatonic_pitch_name = tmp(self._chromatic_pitch_name)
      return pitchtools.NamedDiatonicPitch(diatonic_pitch_name)

   @property
   def named_diatonic_pitch_class(self):
      '''Named diatonic pitch-class from named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs''")
         abjad> named_pitch.named_diatonic_pitch_class
         NamedDiatonicPitchClass('c')
      '''
      from abjad.tools import pitchtools
      return pitchtools.NamedDiatonicPitchClass(self._diatonic_pitch_class_name)
   
   @property
   def named_pitch_class(self):
      '''New named pitch class from named pitch::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.named_pitch_class
         NamedChromaticPitchClass(cs)

      Return named pitch class.
      '''
      from abjad.tools import pitchtools
      if self._pitch_class_name is not None:
         return pitchtools.NamedChromaticPitchClass(self._pitch_class_name)
      else:
         return None

   @property
   def pitch_number(self):
      '''Read-only pitch number of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.pitch_number
         1
      '''
      from abjad.tools.pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number import \
         diatonic_pitch_class_name_to_chromatic_pitch_class_number
      if not self.octave_number is None:
         if self.diatonic_pitch_class_name:
            if self.accidental:
               octave = 12 * (self.octave_number - 4)
               pc = diatonic_pitch_class_name_to_chromatic_pitch_class_number(self.diatonic_pitch_class_name)
               semitones = self.accidental.semitones
               return octave + pc + semitones
      else:
         return None

   @property
   def octave_number(self):
      '''Read-only integer octave number of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.octave_number
         4
      '''
      #return self._octave_number
      from abjad.tools import pitchtools
      from abjad.tools.pitchtools.is_chromatic_pitch_name import chromatic_pitch_name_regex
      groups = chromatic_pitch_name_regex.match(self._chromatic_pitch_name).groups( )
      octave_tick_string = groups[-1]
      return pitchtools.octave_tick_string_to_octave_number(octave_tick_string)

   @property
   def numbered_diatonic_pitch(self):
      '''Numeric diatonic pitch from named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs''")
         abjad> named_pitch.numbered_diatonic_pitch
         NumberedDiatonicPitch(7)
      '''
      from abjad.tools import pitchtools
      name_and_ticks = self._diatonic_pitch_class_name
      name_and_ticks += self._octave_tick_string
      return pitchtools.NumberedDiatonicPitch(name_and_ticks)

   @property
   def numbered_diatonic_pitch_class(self):
      '''Numeric diatonic pitch from named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs''")
         abjad> named_pitch.numbered_diatonic_pitch_class
         NumberedDiatonicPitchClass(0)
      '''
      from abjad.tools import pitchtools
      return pitchtools.NumberedDiatonicPitchClass(self._diatonic_pitch_class_name)

   @property
   def numbered_chromatic_pitch_class(self):
      '''New numeric pitch-class from named pitch::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.numbered_chromatic_pitch_class
         NumberedChromaticPitchClass(1)
   
      Return numeric pitch class.
      '''
      from abjad.tools import pitchtools
      number = self.pitch_number
      if number is not None:
         return pitchtools.NumberedChromaticPitchClass(number % 12)
      else:
         return None

   @property
   def semitones(self):
      '''Read-only semitones of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedChromaticPitch("cs'")
         abjad> named_pitch.semitones
         1
      '''
      return self.pitch_number
