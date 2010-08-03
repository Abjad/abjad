from abjad.Pitch import Pitch
from abjad.tools.pitchtools.get_pitch import get_pitch
from abjad.tools.pitchtools.Accidental import Accidental


class NamedPitchClass(object):
   '''.. versionadded:: 1.1.2

   Named pitch-class ranging over c, cqs, cs, ..., bf, bqf, b. 
   '''

   def __init__(self, arg):
      if isinstance(arg, str):
         self._init_by_name_string(arg)
      elif isinstance(arg, NamedPitchClass):
         self._init_by_name_string(arg.name)
      else:
         pitch = get_pitch(arg)
         self._name = pitch.name

   ## OVERLOADS ##

   def __add__(self, melodic_diatonic_interval):
      from abjad.Pitch import Pitch
      from abjad.tools import pitchtools
      dummy = Pitch(self.name, 4)
      mdi = melodic_diatonic_interval
      new = pitchtools.transpose_by_melodic_diatonic_interval(dummy, mdi)
      return new.named_pitch_class

   def __copy__(self):
      return NamedPitchClass(self)

   def __eq__(self, arg):
      if isinstance(arg, NamedPitchClass):
         return self.name == arg.name
      return False

   def __ge__(self, arg):
      if not isinstance(arg, NamedPitchClass):
         raise TypeError
      if self._letter_string == arg._letter_string:
         return self.numeric_pitch_class >= arg.numeric_pitch_class
      else:
         return self._letter_string >= arg._letter_string

   def __gt__(self, arg):
      if not isinstance(arg, NamedPitchClass):
         raise TypeError
      if self._letter_string == arg._letter_string:
         return self.numeric_pitch_class > arg.numeric_pitch_class
      else:
         return self._letter_string > arg._letter_string

   def __hash__(self):
      return hash(repr(self))

   def __le__(self, arg):
      if not isinstance(arg, NamedPitchClass):
         raise TypeError
      if self._letter_string == arg._letter_string:
         return self.numeric_pitch_class <= arg.numeric_pitch_class
      else:
         return self._letter_string <= arg._letter_string

   def __lt__(self, arg):
      if not isinstance(arg, NamedPitchClass):
         raise TypeError
      if self._letter_string == arg._letter_string:
         return self.numeric_pitch_class < arg.numeric_pitch_class
      else:
         return self._letter_string < arg._letter_string

   def __ne__(self, arg):
      return not self == arg
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.name)

   def __str__(self):
      return '%s' % self.name

   def __sub__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError('%s must be named pitch class.' % arg)
      from abjad.Pitch import Pitch
      from abjad.tools import pitchtools
      pitch_1 = Pitch(self, 4)
      pitch_2 = Pitch(arg, 4)
      mdi = pitchtools.melodic_diatonic_interval_from_to(pitch_1, pitch_2)
      dic = pitchtools.DiatonicIntervalClass(mdi.quality_string, mdi.number)
      return dic

   ## PRIVATE ATTRIBUTES ##

   @property
   def _accidental_string(self):
      return self.name[1:]

   @property
   def _letter_string(self):
      return self.name[0]

   ## PRIVATE METHODS ##

   def _init_by_name_string(self, name):
      if not self._is_acceptable_name(name.lower( )):
         raise ValueError("unknown pitch-class name '%s'." % name)
      self._name = name.lower( )

   def _is_acceptable_name(self, name):
      return name in (
         'c', 'cf', 'cs', 'cqf', 'cqs', 'ctqf', 'ctqs', 'cff', 'css',
         'd', 'df', 'ds', 'dqf', 'dqs', 'dtqf', 'dtqs', 'dff', 'dss',
         'e', 'ef', 'es', 'eqf', 'eqs', 'etqf', 'etqs', 'eff', 'ess',
         'f', 'ff', 'fs', 'fqf', 'fqs', 'ftqf', 'ftqs', 'fff', 'fss',
         'g', 'gf', 'gs', 'gqf', 'gqs', 'gtqf', 'gtqs', 'gff', 'gss',
         'a', 'af', 'as', 'aqf', 'aqs', 'atqf', 'atqs', 'aff', 'ass',
         'b', 'bf', 'bs', 'bqf', 'bqs', 'btqf', 'btqs', 'bff', 'bss')

   ## PUBLIC ATTRIBUTES ##

   @property
   def accidental(self):
      '''Read-only accidental string of pitch-class name.'''
      return Accidental(self.name[1:])

   @property
   def letter(self):
      '''Read-only first letter of pitch-class name.'''
      return self.name[0]

   @property
   def name(self):
      '''Read-only name of pitch-class.'''
      return self._name

   @property
   def numeric_pitch_class(self):
      '''Read-only numeric pitch-class.'''
      pitch = Pitch(self.name, 4)
      return pitch.pitch_class

   @property
   def symbolic_name(self):
      '''Read-only letter plus punctuation of pitch name.'''
      accidental_to_symbol = {
         '': '', 's': '#', 'f': 'b', 'ss': '##', 'ff': 'bb',
         'qs': 'qs', 'qf': 'qf', 'tqs': 'tqs', 'tqf': 'tqf'}
      symbol = accidental_to_symbol[self.accidental.alphabetic_string]
      return self.letter + symbol

   ## PUBLIC METHODS ##

   def apply_accidental(self, accidental):
      '''Apply accidental and emit new named pitch class instance.'''
      accidental = Accidental(accidental)
      new_accidental = self.accidental + accidental
      new_name = self.letter + new_accidental.alphabetic_string
      return type(self)(new_name)

   def transpose(self, mdi):
      '''Transpose pitch class by melodic diatonic interval.'''
      from abjad.Pitch import Pitch
      from abjad.tools.pitchtools.transpose_by_melodic_diatonic_interval \
         import transpose_by_melodic_diatonic_interval
      pitch = Pitch(self, 4)
      transposed_pitch = transpose_by_melodic_diatonic_interval(pitch, mdi)
      transposed_named_pitch_class = transposed_pitch.named_pitch_class
      return transposed_named_pitch_class
