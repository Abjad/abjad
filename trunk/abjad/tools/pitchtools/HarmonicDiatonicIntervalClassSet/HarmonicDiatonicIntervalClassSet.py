from abjad.tools.pitchtools.HarmonicDiatonicIntervalClass import \
   HarmonicDiatonicIntervalClass


class HarmonicDiatonicIntervalClassSet(set):
   '''.. versionadded:: 1.1.2

   Unordered collection of harmonic diatonic interval class instances.
   '''

   def __init__(self, interval_tokens):
      self.update(interval_tokens)

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
      
   ## PUBLIC METHODS ##

   def add(self, arg):
      interval_class = HarmonicDiatonicIntervalClass(arg)
      set.add(self, interval_class)

   def update(self, expr):
      for x in expr:
         self.add(x)
