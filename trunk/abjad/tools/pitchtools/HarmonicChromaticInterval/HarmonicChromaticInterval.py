from abjad.tools.pitchtools._ChromaticInterval import _ChromaticInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval
from abjad.tools.pitchtools.HarmonicChromaticIntervalClass import HarmonicChromaticIntervalClass


class HarmonicChromaticInterval(_ChromaticInterval, _HarmonicInterval):
   '''.. versionadded:: 1.1.2

   Harmonic chromatic interval. ::

      abjad> pitchtools.HarmonicChromaticInterval(-2)
      HarmonicChromaticInterval(2)
   '''

   def __init__(self, number):
      _ChromaticInterval.__init__(self, number)
      self._number = abs(self.number)

   ## OVERLOADS ##

   def __ge__(self, arg):
      if not isinstance(arg, HarmonicChromaticInterval):
         raise TypeError('%s must be harmonic chromatic interval.' % arg)
      return self.number >= arg.number

   def __gt__(self, arg):
      if not isinstance(arg, HarmonicChromaticInterval):
         raise TypeError('%s must be harmonic chromatic interval.' % arg)
      return self.number > arg.number

   def __le__(self, arg):
      if not isinstance(arg, HarmonicChromaticInterval):
         raise TypeError('%s must be harmonic chromatic interval.' % arg)
      return self.number <= arg.number

   def __lt__(self, arg):
      if not isinstance(arg, HarmonicChromaticInterval):
         raise TypeError('%s must be harmonic chromatic interval.' % arg)
      return self.number < arg.number

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class(self):
      #return self.number % 12
      return HarmonicChromaticIntervalClass(self)
