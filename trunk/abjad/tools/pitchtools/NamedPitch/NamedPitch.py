from abjad.cfg._read_config_file import _read_config_file
from abjad.tools.pitchtools._Pitch import _Pitch


_accidental_spelling = _read_config_file( )['accidental_spelling']

class NamedPitch(_Pitch):
   '''Abjad model of named pitch:

   ::

      abjad> pitchtools.NamedPitch("cs'")
      NamedPitch("cs'")
   '''

   accidental_spelling = _accidental_spelling

   __slots__ = ('_accidental', '_deviation', '_diatonic_pitch_class_name', '_octave')

   def __new__(klass, *args, **kwargs):
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      _deviation = kwargs.get('deviation', None)
      object.__setattr__(self, '_deviation', _deviation)
      if not args:
         self._init_empty( )
      elif len(args) == 1 and isinstance(args[0], (int, long, float)):
         self._init_by_number(*args)
      elif len(args) == 1 and isinstance(args[0], type(self)):
         self._init_by_reference(*args)
      elif len(args) == 1 and hasattr(args[0], 'named_pitch'):
         self._init_by_reference(args[0].named_pitch)
      elif len(args) == 1 and pitchtools.is_named_pitch_pair(args[0]):
         self._init_by_pair(*args)
      elif len(args) == 1 and isinstance(args[0], str):
         self._init_by_pitch_string(*args)
      elif len(args) == 2 and isinstance(args[0], str):
         self._init_by_name_and_octave(*args)
      elif len(args) == 2 and isinstance(args[0], pitchtools.NamedPitchClass):
         self._init_by_named_pitch_class_and_octave_number(*args)
      elif len(args) == 2 and isinstance(args[0], (int, long, float)):
         if isinstance(args[1], str):
            self._init_by_number_and_letter(*args)
         elif isinstance(args[1], pitchtools.NamedPitchClass):
            self._init_by_number_and_named_pitch_class(*args)
         else:
            raise TypeError
      elif len(args) == 3:
         self._init_by_name_octave_and_deviation(*args)
      else:
         raise ValueError('\n\tNot a valid pitch token: "%s".' % str(args))
      return self

   def __getnewargs__(self):
      return (self._pitch_class_name, self.octave_number)

   ## OVERLOADS ##

   def __add__(self, melodic_interval):
      '''.. versionadded:: 1.1.2'''
      from abjad.tools import pitchtools
      return pitchtools.transpose_pitch_by_melodic_interval(self, melodic_interval)

   def __copy__(self):
      '''.. versionadded:: 1.1.2'''
      return type(self)(self)

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.diatonic_pitch_number == arg.diatonic_pitch_number:
            if self.accidental.semitones == arg.accidental.semitones:
               if self.deviation == arg.deviation:
                  return True
      return False

   def __ge__(self, arg):
      if not isinstance(arg, type(self)):
         return False
      return self.diatonic_pitch_number > arg.diatonic_pitch_number or \
         (self.diatonic_pitch_number == arg.diatonic_pitch_number and \
         self.accidental.semitones >= arg.accidental.semitones) or \
         (self.diatonic_pitch_number == arg.diatonic_pitch_number and \
         self.accidental == arg.accidental and \
         self._deviation_numeric >= arg._deviation_numeric)

   def __gt__(self, arg):
      if not isinstance(arg, type(self)):
         return False
      return self.diatonic_pitch_number > arg.diatonic_pitch_number or \
         (self.diatonic_pitch_number == arg.diatonic_pitch_number and \
         self.accidental.semitones > arg.accidental.semitones) or \
         (self.diatonic_pitch_number == arg.diatonic_pitch_number and \
         self.accidental == arg.accidental and \
         self._deviation_numeric > arg._deviation_numeric)

   def __hash__(self):
      return hash(repr(self))

   def __le__(self, arg):
      if not isinstance(arg, type(self)):
         return False
      if not self.diatonic_pitch_number == arg.diatonic_pitch_number:
         return self.diatonic_pitch_number <= arg.diatonic_pitch_number
      if not self.accidental == arg.accidental:
         return self.accidental <= arg.accidental
      return self._deviation_numeric <= arg._deviation_numeric

   def __lt__(self, arg):
      if not isinstance(arg, type(self)):
         return False
      return self.diatonic_pitch_number < arg.diatonic_pitch_number or \
         (self.diatonic_pitch_number == arg.diatonic_pitch_number and \
         self.accidental.semitones < arg.accidental.semitones) or \
         (self.diatonic_pitch_number == arg.diatonic_pitch_number and \
         self.accidental == arg.accidental and \
         self._deviation_numeric < arg._deviation_numeric)

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
         return '%s%s' % (self._pitch_class_name, self._ticks_string)
      else:
         return ''

   def __sub__(self, arg):
      from abjad.tools import pitchtools
      if isinstance(arg, type(self)):
         return pitchtools.calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch(
            self, arg)
      else:
         interval = arg
         return pitchtools.transpose_pitch_by_melodic_interval(self, -interval)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _deviation_numeric(self):
      if self.deviation is None:
         return 0
      else:
         return self.deviation

   @property
   def _ticks_string(self):
      '''Read-only octave tick string of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch._ticks_string
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

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.pitch_class_name
         'cs'
      '''
      if self.diatonic_pitch_class_name and self.accidental:
         return '%s%s' % (self.diatonic_pitch_class_name, self.accidental)
      else:
         return None

   ## PRIVATE METHODS ##

   def _init_by_name_and_octave(self, name, octave):
      from abjad.tools import pitchtools
      diatonic_pitch_class_name = name[0]
      accidental_string = name[1:]
      object.__setattr__(self, '_diatonic_pitch_class_name', diatonic_pitch_class_name)
      object.__setattr__(self, '_accidental', pitchtools.Accidental(accidental_string))
      object.__setattr__(self, '_octave', octave)

   def _init_by_name_octave_and_deviation(self, name, octave, deviation):
      self._init_by_name_and_octave(name, octave)
      object.__setattr__(self, '_deviation', deviation)

   def _init_by_named_pitch_class_and_octave_number(self, npc, octave_number):
      self._init_by_name_and_octave(npc.name, octave_number)

   def _init_by_number(self, number):
      from abjad.tools import pitchtools
      spelling = self.accidental_spelling
      triple = pitchtools.pitch_number_to_pitch_letter_alphabetic_accidental_string_and_octave_number_triple(number, spelling)
      diatonic_pitch_class_name, accidental_string, octave = triple
      object.__setattr__(self, '_diatonic_pitch_class_name', diatonic_pitch_class_name)
      object.__setattr__(self, '_accidental', pitchtools.Accidental(accidental_string))
      object.__setattr__(self, '_octave', octave)

   def _init_by_number_and_letter(self, number, diatonic_pitch_class_name):
      from abjad.tools import pitchtools
      pair = pitchtools.number_letter_to_accidental_octave(number, diatonic_pitch_class_name)
      accidental_string, octave = pair
      object.__setattr__(self, '_diatonic_pitch_class_name', diatonic_pitch_class_name)
      object.__setattr__(self, '_accidental', pitchtools.Accidental(accidental_string))
      object.__setattr__(self, '_octave', octave)

   def _init_by_number_and_named_pitch_class(self, pitch_number, npc):
      diatonic_pitch_class_name = npc.name[:1]
      self._init_by_number_and_letter(pitch_number, diatonic_pitch_class_name)

   def _init_by_pair(self, pair):
      from abjad.tools import pitchtools
      name, octave = pair
      diatonic_pitch_class_name = name[0]
      accidental_string = name[1:]
      object.__setattr__(self, '_diatonic_pitch_class_name', diatonic_pitch_class_name)
      object.__setattr__(self, '_accidental', pitchtools.Accidental(accidental_string))
      object.__setattr__(self, '_octave', octave)

   def _init_by_pitch_string(self, pitch_string):
      from abjad.tools import pitchtools
      name = pitchtools.pitch_name_to_pitch_class_name(pitch_string)
      octave_number = pitchtools.pitch_name_to_octave_number(pitch_string)
      self._init_by_name_and_octave(name, octave_number)

   def _init_by_reference(self, pitch):
      from abjad.tools import pitchtools
      object.__setattr__(self, '_diatonic_pitch_class_name', pitch.diatonic_pitch_class_name)
      accidental = pitchtools.Accidental(pitch.accidental.alphabetic_string)
      object.__setattr__(self, '_accidental', accidental)
      object.__setattr__(self, '_octave', pitch.octave_number)

   def _init_empty(self):
      raise ValueError('\n\tEmpty pitch not allowed.')

   ## PUBLIC ATTRIBUTES ##

   @property
   def accidental(self):
      '''Read-only accidental of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.accidental
         Accidental('s')
      '''
      return self._accidental

   @property
   def deviation(self):
      '''Read-only deviation of named pitch in cents:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.deviation is None
         True
      '''
      return self._deviation

   @property
   def diatonic_pitch_number(self):
      '''Read-only diatonic pitch number of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.diatonic_pitch_number
         0
      '''
      if self.diatonic_pitch_class_name:
         return (self.octave_number - 4) * 7 + self.diatonic_pitch_class_number
      else:
         return None

   @property
   def diatonic_pitch_class_number(self):
      '''Read-only diatonic pitch-class number of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
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

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.format
         "cs'"
      '''
      return str(self)

   @property
   def diatonic_pitch_class_name(self):
      '''Read-only diatonic pitch-class name of pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.diatonic_pitch_class_name
         'c'
      '''
      return self._diatonic_pitch_class_name

   @property
   def named_diatonic_pitch(self):
      '''Named diatonic pitch from named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs''")
         abjad> named_pitch.named_diatonic_pitch
         NamedDiatonicPitch("c''")
      '''
      from abjad.tools import pitchtools
      name_and_ticks = self._diatonic_pitch_class_name
      name_and_ticks += self._ticks_string
      return pitchtools.NamedDiatonicPitch(name_and_ticks)

   @property
   def named_diatonic_pitch_class(self):
      '''Named diatonic pitch-class from named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs''")
         abjad> named_pitch.named_diatonic_pitch_class
         NamedDiatonicPitchClass('c')
      '''
      from abjad.tools import pitchtools
      return pitchtools.NamedDiatonicPitchClass(self._diatonic_pitch_class_name)
   
   @property
   def named_pitch_class(self):
      '''New named pitch class from named pitch::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.named_pitch_class
         NamedPitchClass(cs)

      Return named pitch class.
      '''
      from abjad.tools import pitchtools
      if self._pitch_class_name is not None:
         return pitchtools.NamedPitchClass(self._pitch_class_name)
      else:
         return None

   @property
   def pitch_number(self):
      '''Read-only pitch number of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.pitch_number
         1
      '''
      from abjad.tools.pitchtools.pitch_letter_to_pitch_class_number import \
         pitch_letter_to_pitch_class_number
      if not self.octave_number is None:
         if self.diatonic_pitch_class_name:
            if self.accidental:
               octave = 12 * (self.octave_number - 4)
               pc = pitch_letter_to_pitch_class_number(self.diatonic_pitch_class_name)
               semitones = self.accidental.semitones
               return octave + pc + semitones
      else:
         return None

   @property
   def octave_number(self):
      '''Read-only integer octave number of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.octave_number
         4
      '''
      return self._octave

   @property
   def numeric_diatonic_pitch(self):
      '''Numeric diatonic pitch from named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs''")
         abjad> named_pitch.numeric_diatonic_pitch
         NumericDiatonicPitch(7)
      '''
      from abjad.tools import pitchtools
      name_and_ticks = self._diatonic_pitch_class_name
      name_and_ticks += self._ticks_string
      return pitchtools.NumericDiatonicPitch(name_and_ticks)

   @property
   def numeric_diatonic_pitch_class(self):
      '''Numeric diatonic pitch from named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs''")
         abjad> named_pitch.numeric_diatonic_pitch_class
         NumericDiatonicPitchClass(0)
      '''
      from abjad.tools import pitchtools
      return pitchtools.NumericDiatonicPitchClass(self._diatonic_pitch_class_name)

   @property
   def numeric_pitch_class(self):
      '''New numeric pitch-class from named pitch::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.numeric_pitch_class
         NumericPitchClass(1)
   
      Return numeric pitch class.
      '''
      from abjad.tools import pitchtools
      number = self.pitch_number
      if number is not None:
         return pitchtools.NumericPitchClass(number % 12)
      else:
         return None

   @property
   def semitones(self):
      '''Read-only semitones of named pitch:

      ::

         abjad> named_pitch = pitchtools.NamedPitch("cs'")
         abjad> named_pitch.semitones
         1
      '''
      return self.pitch_number
