from abjad.tools.pitchtools.HarmonicChromaticIntervalSet import \
   HarmonicChromaticIntervalSet
from abjad.tools.pitchtools.HarmonicDiatonicInterval import \
   HarmonicDiatonicInterval


class HarmonicDiatonicIntervalSet(set):
   '''.. versionadded:: 1.1.2

   Unordered collection of harmonic diatonic interval instances.
   '''

   def __init__(self, interval_tokens):
      self.update(interval_tokens)

   ## OVERLOADS ##

   def __copy__(self):
      return HarmonicDiatonicIntervalSet(self)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '{%s}' % self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in sorted(self.intervals)])

   ## PUBLIC ATTRIBUTES ##

   @property
   def harmonic_chromatic_interval_set(self):
      return HarmonicChromaticIntervalSet(self)

   @property
   def intervals(self):
      return set(self)
      
   @property
   def numbers(self):
      return set([interval.number for interval in self])

   ## PUBLIC METHODS ##

   def add(self, arg):
      interval = HarmonicDiatonicInterval(arg)
      set.add(self, interval)

   def update(self, expr):
      for x in expr:
         self.add(x)
