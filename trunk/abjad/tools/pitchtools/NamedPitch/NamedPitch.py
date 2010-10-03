from abjad.cfg._read_config_file import _read_config_file
from abjad.core import _StrictComparator
from abjad.tools.pitchtools._Pitch import _Pitch


_accidental_spelling = _read_config_file( )['accidental_spelling']

class NamedPitch(_StrictComparator, _Pitch):
   '''Abjad model of named pitch.
   '''

   accidental_spelling = _accidental_spelling

   __slots__ = ('_accidental', '_deviation', '_letter', '_octave')

   def __new__(klass, *args):
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      object.__setattr__(self, '_deviation', None)
      if not args:
         self._init_empty( )
      elif len(args) == 1 and isinstance(args[0], (int, long, float)):
         self._init_by_number(*args)
      elif len(args) == 1 and isinstance(args[0], type(self)):
         self._init_by_reference(*args)
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
         raise ValueError('%s not valid pitch token.' % str(args))
      return self

   def __getnewargs__(self):
      return (self.name, self.octave)

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
      if self.name and not self.octave is None:
         if self.deviation is None:
            return '%s(%s, %s)' % (self.__class__.__name__, self.name, self.octave)
         else:
            return '%s(%s, %s, %s)' % (self.__class__.__name__,
               self.name, self.octave, self.deviation)
      else:
         return '%s( )' % self.__class__.__name__

   def __str__(self):
      if self.name and not self.octave is None:
         return '%s%s' % (self.name, self.ticks)
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

   ## PRIVATE METHODS ##

   def _init_by_name_and_octave(self, name, octave):
      from abjad.tools import pitchtools
      letter = name[0]
      accidental_string = name[1:]
      object.__setattr__(self, '_letter', letter)
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
      letter, accidental_string, octave = triple
      object.__setattr__(self, '_letter', letter)
      object.__setattr__(self, '_accidental', pitchtools.Accidental(accidental_string))
      object.__setattr__(self, '_octave', octave)

   def _init_by_number_and_letter(self, number, letter):
      from abjad.tools import pitchtools
      pair = pitchtools.number_letter_to_accidental_octave(number, letter)
      accidental_string, octave = pair
      object.__setattr__(self, '_letter', letter)
      object.__setattr__(self, '_accidental', pitchtools.Accidental(accidental_string))
      object.__setattr__(self, '_octave', octave)

   def _init_by_number_and_named_pitch_class(self, pitch_number, npc):
      letter = npc.name[:1]
      self._init_by_number_and_letter(pitch_number, letter)

   def _init_by_pair(self, pair):
      from abjad.tools import pitchtools
      name, octave = pair
      letter = name[0]
      accidental_string = name[1:]
      object.__setattr__(self, '_letter', letter)
      object.__setattr__(self, '_accidental', pitchtools.Accidental(accidental_string))
      object.__setattr__(self, '_octave', octave)

   def _init_by_pitch_string(self, pitch_string):
      from abjad.tools import pitchtools
      name = pitchtools.pitch_name_to_pitch_class_name(pitch_string)
      octave_number = pitchtools.pitch_name_to_octave_number(pitch_string)
      self._init_by_name_and_octave(name, octave_number)

   def _init_by_reference(self, pitch):
      from abjad.tools import pitchtools
      object.__setattr__(self, '_letter', pitch.letter)
      accidental = pitchtools.Accidental(pitch.accidental.alphabetic_string)
      object.__setattr__(self, '_accidental', accidental)
      object.__setattr__(self, '_octave', pitch.octave)

   def _init_empty(self):
      object.__setattr__(self, '_letter', None)
      object.__setattr__(self, '_accidental', None)
      object.__setattr__(self, '_octave', None)

   ## PUBLIC ATTRIBUTES ##

   @property
   def accidental(self):
      return self._accidental

   @property
   def degree(self):
      '''Diatonic scale degree with ``1`` for C, ``2`` for D, etc.'''
      from abjad.tools.pitchtools.pitch_letter_to_one_indexed_diatonic_scale_degree_number \
         import pitch_letter_to_one_indexed_diatonic_scale_degree_number
      if self.letter:
         return pitch_letter_to_one_indexed_diatonic_scale_degree_number(self.letter)
      else:
         return None

   @property
   def deviation(self):
      return self._deviation

   @property
   def diatonic_pitch_number(self):
      '''Read-only diatonic pitch number of named pitch.
      '''
      if self.letter:
         return (self.octave - 4) * 7 + self.degree - 1
      else:
         return None

   @property
   def format(self):
      '''Read-only LilyPond format of pitch.'''
      return str(self)

   @property
   def letter(self):
      return self._letter

   @property
   def name(self):
      if self.letter and self.accidental:
         return '%s%s' % (self.letter, self.accidental)
      else:
         return None

   @property
   def named_pitch_class(self):
      from abjad.tools import pitchtools
      return pitchtools.NamedPitchClass(self.name)

   @property
   def number(self):
      '''Read / write numeric value of pitch with middle C equal to ``0``.'''
      from abjad.tools.pitchtools.pitch_letter_to_pitch_class_number import \
         pitch_letter_to_pitch_class_number
      if not self.octave is None:
         if self.letter:
            if self.accidental:
               octave = 12 * (self.octave - 4)
               pc = pitch_letter_to_pitch_class_number(self.letter)
               semitones = self.accidental.semitones
               return octave + pc + semitones
      else:
         return None

   @property
   def octave(self):
      return self._octave

   @property
   def pair(self):
      '''Read-only ``(name, octave)`` pair of pitch.'''
      if self.name and self.octave is not None:
         return (self.name, self.octave)
      else:
         return None

   @property
   def pc(self):
      '''Read-only pitch-class corresponding to pitch.

      .. note:: 
         deprecated. Use `pitch_class` instead.
      '''
      from abjad.tools import pitchtools
      number = self.number
      if number is not None:
         return pitchtools.NumericPitchClass(number % 12)
      else:
         return None
      

   @property
   def pitch_class(self):
      '''Read-only pitch-class corresponding to pitch.

      .. versionchanged:: 1.1.2
         now returns Abjad pitch-class instance instead of number.'''
      from abjad.tools import pitchtools
      number = self.number
      if number is not None:
         return pitchtools.NumericPitchClass(number % 12)
      else:
         return None

   @property
   def semitones(self):
      '''Read-only number of semitones to which pitch is equal.'''
      return self.number

   @property
   def ticks(self):
      '''Read-only European indicator of octave of pitch with
      the octave of middle C equal to a single ``'`` tick.'''
      if self.octave is not None:
         if self.octave <= 2:
            return ',' * (3 - self.octave)
         elif self.octave == 3:
            return ''
         else:
            return "'" * (self.octave - 3)
      else:
         return None
