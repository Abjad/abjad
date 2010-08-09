from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval
from abjad.tools.pitchtools.HarmonicDiatonicIntervalSet import HarmonicDiatonicIntervalSet
from abjad.tools.pitchtools.HarmonicChromaticIntervalSet import HarmonicChromaticIntervalSet
from abjad.tools.pitchtools.MelodicChromaticIntervalSet import MelodicChromaticIntervalSet


class MelodicDiatonicIntervalSet(set):
   '''.. versionadded:: 1.1.2

   Unordered collection of melodic diatonic interval instances.
   '''

   def __init__(self, interval_tokens):
      self.update(interval_tokens)

   ## OVERLOADS ##

   def __copy__(self):
      return MelodicDiatonicIntervalSet(self)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '{%s}' % self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      intervals = list(self.intervals)
      intervals.sort(lambda x, y: cmp(x.number, y.number))
      return ', '.join([str(x) for x in intervals])

   ## PUBLIC ATTRIBUTES ##

   @property
   def harmonic_chromatic_interval_set(self):
      return HarmonicChromaticIntervalSet(self)

   @property
   def harmonic_diatonic_interval_set(self):
      return HarmonicDiatonicIntervalSet(self)

   @property
   def melodic_chromatic_interval_set(self):
      return MelodicChromaticIntervalSet(self)

   @property
   def intervals(self):
      return set(self)
      
   @property
   def numbers(self):
      return set([interval.number for interval in self])

   ## PUBLIC METHODS ##

   def add(self, arg):
      interval = MelodicDiatonicInterval(arg)
      set.add(self, interval)

   def update(self, expr):
      for x in expr:
         self.add(x)
