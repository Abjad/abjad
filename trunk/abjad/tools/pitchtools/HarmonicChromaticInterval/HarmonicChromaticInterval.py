from abjad.tools.pitchtools._ChromaticInterval import _ChromaticInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval


class HarmonicChromaticInterval(_ChromaticInterval, _HarmonicInterval):
   '''.. versionadded:: 1.1.2

   Harmonic chromatic interval. ::

      abjad> pitchtools.HarmonicChromaticInterval(-2)
      HarmonicChromaticInterval(2)
   '''

   def __init__(self, interval_number):
      _ChromaticInterval.__init__(self, interval_number)
      self._interval_number = abs(self.interval_number)

   ## OVERLOADS ##

   def __ge__(self, arg):
      if not isinstance(arg, HarmonicChromaticInterval):
         raise TypeError('%s must be harmonic chromatic interval.' % arg)
      return self.interval_number >= arg.interval_number

   def __gt__(self, arg):
      if not isinstance(arg, HarmonicChromaticInterval):
         raise TypeError('%s must be harmonic chromatic interval.' % arg)
      return self.interval_number > arg.interval_number

   def __le__(self, arg):
      if not isinstance(arg, HarmonicChromaticInterval):
         raise TypeError('%s must be harmonic chromatic interval.' % arg)
      return self.interval_number <= arg.interval_number

   def __lt__(self, arg):
      if not isinstance(arg, HarmonicChromaticInterval):
         raise TypeError('%s must be harmonic chromatic interval.' % arg)
      return self.interval_number < arg.interval_number

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class(self):
      return self.interval_number % 12

   @property
   def number(self):
      return self.interval_number
