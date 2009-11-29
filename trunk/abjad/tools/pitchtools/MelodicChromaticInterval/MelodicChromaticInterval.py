from abjad.tools import mathtools
from abjad.tools.pitchtools._ChromaticInterval import _ChromaticInterval
from abjad.tools.pitchtools._MelodicInterval import _MelodicInterval
from abjad.tools.pitchtools.DiatonicInterval import DiatonicInterval
from abjad.tools.pitchtools.HarmonicChromaticInterval import \
   HarmonicChromaticInterval


class MelodicChromaticInterval(_ChromaticInterval, _MelodicInterval):
   '''.. versionaddedd:: 1.1.2

   Melodic chromatic interval in semitones. ::

      abjad> pitchtools.MelodicChromaticInterval(-2)
      MelodicChromaticInterval(-2)
   '''

   def __init__(self, arg):
      if isinstance(arg, (int, float, long)):
         self._interval_number = arg
      elif isinstance(arg, _Interval):
         self._interval_number = arg.semitones
      else:
         raise TypeError('%s must be number or interval.' % arg)

   ## OVERLOADS ##

   def __abs__(self):
      return self.harmonic_interval

   def __ge__(self, arg):
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.interval_number) >= abs(arg.interval_number)

   def __gt__(self, arg):
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.interval_number) > abs(arg.interval_number)

   def __le__(self, arg):
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.interval_number) <= abs(arg.interval_number)

   def __lt__(self, arg):
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.interval_number) < abs(arg.interval_number)

   def __neg__(self):
      return MelodicChromaticInterval(-self._interval_number)

   ## PUBLIC ATTRIBUTES ##

   @property
   def direction_number(self):
      return mathtools.sign(self.interval_number) 

   @property
   def harmonic_interval(self):
      interval_number = abs(self.interval_number)
      return HarmonicChromaticInterval(interval_number)

   @property
   def interval_class(self):
      return self.direction_number * (abs(self.interval_number) % 12)
