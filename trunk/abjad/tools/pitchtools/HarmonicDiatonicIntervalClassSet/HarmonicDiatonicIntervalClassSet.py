from abjad.tools.pitchtools._IntervalClassSet import _IntervalClassSet
from abjad.tools.pitchtools.HarmonicDiatonicIntervalClass import HarmonicDiatonicIntervalClass


class HarmonicDiatonicIntervalClassSet(_IntervalClassSet):
   '''.. versionadded:: 1.1.2

   Abjad model of harmonic diatonic interval-class set.

   Harmonic diatonic interval-class sets are immutable.
   '''

   #def __init__(self, interval_tokens):
   def __new__(self, interval_tokens):
      #self.update(interval_tokens)
      hdics = [HarmonicDiatonicIntervalClass(x) for x in interval_tokens]
      return frozenset.__new__(self, hdics)

   ## OVERLOADS ##

   def __copy__(self):
      return HarmonicDiatonicIntervalClassSet(self)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '{%s}' % self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in sorted(self.interval_classes)])

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_classes(self):
      return set(self)
