from abjad.cfg._read_config_file import _read_config_file
from abjad.core.abjadcore import _Abjad
import types


_accidental_spelling = _read_config_file( )['accidental_spelling']

class Pitch(_Abjad):
   '''Musical pitch.'''

   accidental_spelling = _accidental_spelling

   def __init__(self, *args):
      from abjad.tools import pitchtools
      self._deviation = None
      if not args:
         self._init_empty( )
      elif len(args) == 1 and isinstance(args[0], (int, long, float)):
         self._init_by_number(*args)
      elif len(args) == 1 and isinstance(args[0], Pitch):
         self._init_by_reference(*args)
      elif len(args) == 1 and pitchtools.is_pair(args[0]):
         self._init_by_pair(*args)
      elif len(args) == 1 and isinstance(args[0], str):
         self._init_by_pitch_string(*args)
      elif len(args) == 2 and isinstance(args[0], str):
         self._init_by_name_and_octave(*args)
      elif len(args) == 2 and isinstance(args[0], (int, long, float)):
         self._init_by_number_and_letter(*args)
      elif len(args) == 3:
         self._init_by_name_octave_and_deviation(*args)
      else:
         raise ValueError('%s not valid pitch token.' % str(args))

   ## OVERLOADS ##

   def __add__(self, melodic_interval):
      '''.. versionadded:: 1.1.2'''
      from abjad.tools import pitchtools
      return pitchtools.transpose_by_melodic_interval(self, melodic_interval)

   def __copy__(self):
      '''.. versionadded:: 1.1.2'''
      return Pitch(self)

   def __eq__(self, arg):
      if isinstance(arg, Pitch):
         if self.altitude == arg.altitude:
            if self.accidental.semitones == arg.accidental.semitones:
               if self.deviation == arg.deviation:
                  return True
      return False

   def __ge__(self, arg):
      if not isinstance(arg, Pitch):
         raise ValueError
      return self.altitude > arg.altitude or \
         (self.altitude == arg.altitude and \
         self.accidental.semitones >= arg.accidental.semitones) or \
         (self.altitude == arg.altitude and \
         self.accidental == arg.accidental and \
         self._deviation_numeric >= arg._deviation_numeric)

   def __gt__(self, arg):
      if not isinstance(arg, Pitch):
         raise ValueError
      return self.altitude > arg.altitude or \
         (self.altitude == arg.altitude and \
         self.accidental.semitones > arg.accidental.semitones) or \
         (self.altitude == arg.altitude and \
         self.accidental == arg.accidental and \
         self._deviation_numeric > arg._deviation_numeric)

   def __hash__(self):
      return hash(repr(self))

   def __le__(self, arg):
      if not isinstance(arg, Pitch):
         raise ValueError
      if not self.altitude == arg.altitude:
         return self.altitude <= arg.altitude
      if not self.accidental == arg.accidental:
         return self.accidental <= arg.accidental
      return self._deviation_numeric <= arg._deviation_numeric

   def __lt__(self, arg):
      if not isinstance(arg, Pitch):
         raise ValueError
      return self.altitude < arg.altitude or \
         (self.altitude == arg.altitude and \
         self.accidental.semitones < arg.accidental.semitones) or \
         (self.altitude == arg.altitude and \
         self.accidental == arg.accidental and \
         self._deviation_numeric < arg._deviation_numeric)

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      if self.name and not self.octave is None:
         if self.deviation is None:
            return 'Pitch(%s, %s)' % (self.name, self.octave)
         else:
            return 'Pitch(%s, %s, %s)' % (
               self.name, self.octave, self.deviation)
      else:
         return 'Pitch( )'

   def __str__(self):
      if self.name and not self.octave is None:
         return '%s%s' % (self.name, self.ticks)
      else:
         return ''

   def __sub__(self, arg):
      from abjad.tools import pitchtools
      if isinstance(arg, Pitch):
         return pitchtools.melodic_diatonic_interval_from_to(self, arg)
      else:
         interval = arg
         return pitchtools.transpose_by_melodic_interval(self, -interval)

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
      self.letter = letter
      self.accidental = pitchtools.Accidental(accidental_string)
      self.octave = octave

   def _init_by_name_octave_and_deviation(self, name, octave, deviation):
      self._init_by_name_and_octave(name, octave)
      self.deviation = deviation

   def _init_by_number(self, number):
      from abjad.tools import pitchtools
      spelling = self.accidental_spelling
      triple = pitchtools.number_to_letter_accidental_octave(number, spelling)
      letter, accidental_string, octave = triple
      self.letter = letter
      self.accidental = pitchtools.Accidental(accidental_string)
      self.octave = octave

   def _init_by_number_and_letter(self, number, letter):
      from abjad.tools import pitchtools
      pair = pitchtools.number_letter_to_accidental_octave(number, letter)
      accidental_string, octave = pair
      self.letter = letter
      self.accidental = pitchtools.Accidental(accidental_string)
      self.octave = octave

   def _init_by_pair(self, pair):
      from abjad.tools import pitchtools
      name, octave = pair
      letter = name[0]
      accidental_string = name[1:]
      self.letter = letter
      self.accidental = pitchtools.Accidental(accidental_string)
      self.octave = octave

   def _init_by_pitch_string(self, pitch_string):
      from abjad.tools import pitchtools
      name = pitchtools.pitch_string_to_name(pitch_string)
      octave_number = pitchtools.pitch_string_to_octave_number(pitch_string)
      self._init_by_name_and_octave(name, octave_number)

   def _init_by_reference(self, pitch):
      from abjad.tools import pitchtools
      self.letter = pitch.letter
      self.accidental = pitchtools.Accidental(pitch.accidental._string)
      self.octave = pitch.octave

   def _init_empty(self):
      self.letter = None
      self.accidental = None
      self.octave = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def absolute_diatonic_scale_degree(self):
      return 7 * self.octave + self.degree

   @apply
   def accidental( ):
      def fget(self):
         '''Read / write reference to any accidental attaching to pitch.'''
         return self._accidental
      def fset(self, expr):
         from abjad.tools import pitchtools
         if expr is None:
            self._accidental = pitchtools.Accidental('')
         elif isinstance(expr, str):
            self._accidental = pitchtools.Accidental(expr)
         elif isinstance(expr, pitchtools.Accidental):
            self._accidental = expr
         else:
            raise ValueError('can not set accidental.')
      return property(**locals( ))

   @property
   def altitude(self):
      '''See :term:`altitude`.'''
      if self.letter:
         return (self.octave - 4) * 7 + self.degree - 1
      else:
         return None
      
   @property
   def degree(self):
      '''Diatonic scale degree with ``1`` for C, ``2`` for D, etc.'''
      from abjad.tools.pitchtools.letter_to_diatonic_scale_degree \
         import letter_to_diatonic_scale_degree
      if self.letter:
         return letter_to_diatonic_scale_degree(self.letter)
      else:
         return None

   @apply
   def deviation( ):
      def fget(self):
         '''Read / write number of cents by which pitch deviates
            from 12-ET intonation.'''
         return self._deviation
      def fset(self, arg):
         assert isinstance(arg, (int, float, types.NoneType))
         self._deviation = arg
      return property(**locals( ))

   @property
   def format(self):
      '''Read-only LilyPond format of pitch.'''
      return str(self)

   @apply
   def name( ):
      def fget(self):
         '''Read / write letter and accidental of pitch concatenated
         as a single string.'''
         if self.letter and self.accidental:
            return '%s%s' % (self.letter, self.accidental)
         else:
            return None
      def fset(self, name):
         from abjad.tools.pitchtools.name_to_letter_accidental \
            import name_to_letter_accidental
         letter, accidental = name_to_letter_accidental(name)
         self.letter = letter
         self.accidental = accidental
      return property(**locals( ))

   @apply
   def number( ):
      def fget(self):
         '''Read / write numeric value of pitch
         with middle C equal to ``0``.'''
         from abjad.tools.pitchtools.letter_to_pc import letter_to_pc
         if not self.octave is None:
            if self.letter:
               if self.accidental:
                  octave = 12 * (self.octave - 4)
                  pc = letter_to_pc(self.letter)
                  semitones = self.accidental.semitones
                  return octave + pc + semitones
         else:
            return None
      def fset(self, arg):
         self.__init__(arg)
      return property(**locals( ))

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
         return pitchtools.PitchClass(number % 12)
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
         return pitchtools.PitchClass(number % 12)
      else:
         return None
      

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
