from abjad.tools.pitchtools._PitchClass import _PitchClass
from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import \
   get_named_chromatic_pitch_from_pitch_carrier


class NamedChromaticPitchClass(_PitchClass):
   '''.. versionadded:: 1.1.2

   Abjad model of named chromatic pitch-class::

      abjad> pitchtools.NamedChromaticPitchClass('cs')
      NamedChromaticPitchClass('cs')

   Named chromatic pitch-classes are immutable.
   '''

   __slots__ = ('_chromatic_pitch_class_name', )

   ## TODO: use __new__ ##

   def __init__(self, arg):
      from abjad.tools import pitchtools
      if hasattr(arg, '_chromatic_pitch_class_name'):
         chromatic_pitch_class_name = arg._chromatic_pitch_class_name
      elif pitchtools.is_chromatic_pitch_name(arg):
         chromatic_pitch_class_name = \
            pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name(arg)
      else:
         try:
            named_chromatic_pitch_carrier = get_named_chromatic_pitch_from_pitch_carrier(arg)
         except (ValueError, TypeError):
            raise ValueError
         if hasattr(named_chromatic_pitch_carrier, '_chromatic_pitch_name'):
            chromatic_pitch_name = named_chromatic_pitch_carrier._chromatic_pitch_name
         elif hasattr(named_chromatic_pitch_carrier, 'pitch'):
            named_chromatic_pitch = named_chromatic_pitch_carrier.pitch
            chromatic_pitch_name = named_chromatic_pitch._chromatic_pitch_name
         else:
            raise TypeError
         chromatic_pitch_class_name = \
            pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name(chromatic_pitch_name)
      chromatic_pitch_class_name = chromatic_pitch_class_name.lower( )
      object.__setattr__(self, '_chromatic_pitch_class_name', chromatic_pitch_class_name)

   ## OVERLOADS ##

   def __add__(self, melodic_diatonic_interval):
      from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
      from abjad.tools import pitchtools
      dummy = NamedChromaticPitch(self.name, 4)
      mdi = melodic_diatonic_interval
      new = pitchtools.transpose_pitch_carrier_by_melodic_diatonic_interval(dummy, mdi)
      return new.named_chromatic_pitch_class

   def __copy__(self):
      return NamedChromaticPitchClass(self)

   def __eq__(self, arg):
      if isinstance(arg, NamedChromaticPitchClass):
         return self.name == arg.name
      return False

   def __ge__(self, arg):
      if not isinstance(arg, NamedChromaticPitchClass):
         raise TypeError
      if self._letter_string == arg._letter_string:
         return self.numbered_chromatic_pitch_class >= arg.numbered_chromatic_pitch_class
      else:
         return self._letter_string >= arg._letter_string

   def __gt__(self, arg):
      if not isinstance(arg, NamedChromaticPitchClass):
         raise TypeError
      if self._letter_string == arg._letter_string:
         return self.numbered_chromatic_pitch_class > arg.numbered_chromatic_pitch_class
      else:
         return self._letter_string > arg._letter_string

   def __hash__(self):
      return hash(repr(self))

   def __le__(self, arg):
      if not isinstance(arg, NamedChromaticPitchClass):
         raise TypeError
      if self._letter_string == arg._letter_string:
         return self.numbered_chromatic_pitch_class <= arg.numbered_chromatic_pitch_class
      else:
         return self._letter_string <= arg._letter_string

   def __lt__(self, arg):
      if not isinstance(arg, NamedChromaticPitchClass):
         raise TypeError
      if self._letter_string == arg._letter_string:
         return self.numbered_chromatic_pitch_class < arg.numbered_chromatic_pitch_class
      else:
         return self._letter_string < arg._letter_string

   def __ne__(self, arg):
      return not self == arg
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._repr_string)

   def __str__(self):
      return '%s' % self.name

   def __sub__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError('%s must be named pitch class.' % arg)
      from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
      from abjad.tools import pitchtools
      pitch_1 = NamedChromaticPitch(self, 4)
      pitch_2 = NamedChromaticPitch(arg, 4)
      mdi = pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(
         pitch_1, pitch_2)
      dic = pitchtools.InversionEquivalentDiatonicIntervalClass(mdi.quality_string, mdi.number)
      return dic

   ## PRIVATE ATTRIBUTES ##

   @property
   def _accidental_string(self):
      return self.name[1:]

   @property
   def _letter_string(self):
      return self.name[0]

   @property
   def _repr_string(self):
      return repr(self.name)

   ## PRIVATE METHODS ##

   def _init_by_name_string(self, name):
      if not self._is_acceptable_name(name.lower( )):
         raise ValueError("unknown pitch-class name '%s'." % name)
      object.__setattr__(self, '_chromatic_pitch_class_name', name.lower( ))

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
      return self._chromatic_pitch_class_name

   @property
   def numbered_chromatic_pitch_class(self):
      '''Read-only numeric pitch-class.'''
      pitch = NamedChromaticPitch(self.name, 4)
      return pitch.numbered_chromatic_pitch_class

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
      from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
      from abjad.tools.pitchtools.transpose_pitch_carrier_by_melodic_diatonic_interval \
         import transpose_pitch_carrier_by_melodic_diatonic_interval
      pitch = NamedChromaticPitch(self, 4)
      transposed_pitch = transpose_pitch_carrier_by_melodic_diatonic_interval(pitch, mdi)
      transposed_named_chromatic_pitch_class = transposed_pitch.named_chromatic_pitch_class
      return transposed_named_chromatic_pitch_class
