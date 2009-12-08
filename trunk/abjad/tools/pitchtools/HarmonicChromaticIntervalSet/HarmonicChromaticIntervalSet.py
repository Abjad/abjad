from abjad.tools.pitchtools.HarmonicChromaticInterval import \
   HarmonicChromaticInterval


class HarmonicChromaticIntervalSet(set):
   '''.. versionadded:: 1.1.2

   Unordered collection of harmonic chromatic interval instances.
   '''

   def __init__(self, interval_tokens):
      self.update(interval_tokens)

   ## OVERLOADS ##

   def __copy__(self):
      return HarmonicChromaticIntervalSet(self)

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
   def intervals(self):
      return set(self)
      
   @property
   def numbers(self):
      return set([interval.number for interval in self])

   ## PUBLIC METHODS ##

   def add(self, arg):
      interval = HarmonicChromaticInterval(arg)
      set.add(self, interval)

   def update(self, expr):
      for x in expr:
         self.add(x)
