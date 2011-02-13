from abjad.tools.pitchtools._ChromaticInterval import _ChromaticInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval
from abjad.tools.pitchtools.HarmonicChromaticIntervalClass import HarmonicChromaticIntervalClass


class HarmonicChromaticInterval(_ChromaticInterval, _HarmonicInterval):
   '''.. versionadded:: 1.1.2

   Abjad model of harmonic chromatic interval::

      abjad> pitchtools.HarmonicChromaticInterval(-14)
      HarmonicChromaticInterval(14)

   Harmonic chromatic intervals are immutable.
   '''

   def __init__(self, number):
      _ChromaticInterval.__init__(self, number)
      _number = abs(self.number)
      object.__setattr__(self, '_number', _number)

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
   def harmonic_chromatic_interval_class(self):
      '''New harmonic chromatic interval-class from harmonic chromatic interval:

      ::

         abjad> harmonic_chromatic_interval = pitchtools.HarmonicChromaticInterval(14)
         abjad> harmonic_chromatic_interval.harmonic_chromatic_interval_class
         HarmonicChromaticIntervalClass(2)
      '''
      return HarmonicChromaticIntervalClass(self)
