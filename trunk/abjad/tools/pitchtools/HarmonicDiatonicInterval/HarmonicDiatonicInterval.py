from abjad.tools import mathtools
from abjad.tools.pitchtools._DiatonicInterval import _DiatonicInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval
from abjad.tools.pitchtools.HarmonicCounterpointInterval import HarmonicCounterpointInterval
from abjad.tools.pitchtools.HarmonicDiatonicIntervalClass import HarmonicDiatonicIntervalClass


class HarmonicDiatonicInterval(_DiatonicInterval, _HarmonicInterval):
   '''.. versionadded:: 1.1.2

   Abjad model harmonic diatonic interval::

      abjad> pitchtools.HarmonicDiatonicInterval('M9')
      HarmonicDiatonicInterval('M9')

   Harmonic diatonic intervals are immutable.
   '''

   def __init__(self, *args):
      from abjad.tools.pitchtools.is_harmonic_diatonic_interval_abbreviation import \
         harmonic_diatonic_interval_abbreviation_regex
      if len(args) == 1 and isinstance(args[0], _DiatonicInterval):
         _quality_string = args[0].quality_string
         _number = abs(args[0].number)
      elif len(args) == 1 and isinstance(args[0], str):
         match = harmonic_diatonic_interval_abbreviation_regex.match(args[0])
         if match is None:
            raise ValueError('"%s" does not have the form of an hdi abbreviation.' % args[0])
         quality_abbreviation, number_string = match.groups( )
         _quality_string = self._quality_abbreviation_to_quality_string[quality_abbreviation]
         _number = int(number_string)
      elif len(args) == 2:
         _quality_string = args[0]
         _number = abs(args[1])
      _DiatonicInterval.__init__(self, _quality_string, _number)

   ## OVERLOADS ##

   def __copy__(self):
      return type(self)(self.quality_string, self.number)

   def __ge__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError
      if self.number == arg.number:
         return self.semitones >= arg.semitones
      return self.number >= arg.number

   def __gt__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError
      if self.number == arg.number:
         return self.semitones > arg.semitones
      return self.number > arg.number

   def __le__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError
      if self.number == arg.number:
         return self.semitones <= arg.semitones
      return self.number <= arg.number

   def __lt__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError
      if self.number == arg.number:
         return self.semitones < arg.semitones
      return self.number < arg.number

   def __repr__(self):
      return "%s('%s')" % (self.__class__.__name__, str(self))

   def __str__(self):
      return '%s%s' % (self._quality_abbreviation, self.number)

   ## PUBLIC ATTRIBUTES ##

   @property
   def counterpoint_interval(self):
      return HarmonicCounterpointInterval(self)

   @property
   def interval_class(self):
      return HarmonicDiatonicIntervalClass(self)

   @property
   def melodic_diatonic_interval_ascending(self):
      from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval
      return MelodicDiatonicInterval(self.quality_string, self.number)

   @property
   def melodic_diatonic_interval_descending(self):
      return -self.melodic_diatonic_interval_ascending

   @property
   def staff_spaces(self):
      if self.quality_string == 'perfect' and self.number == 1:
         return 0
      return abs(_DiatonicInterval.staff_spaces.fget(self))
