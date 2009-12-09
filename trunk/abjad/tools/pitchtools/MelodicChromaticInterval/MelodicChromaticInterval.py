from abjad.tools import mathtools
from abjad.tools.pitchtools._ChromaticInterval import _ChromaticInterval
from abjad.tools.pitchtools._Interval import _Interval
from abjad.tools.pitchtools._MelodicInterval import _MelodicInterval
from abjad.tools.pitchtools.HarmonicChromaticInterval import \
   HarmonicChromaticInterval
from abjad.tools.pitchtools.MelodicChromaticIntervalClass import \
   MelodicChromaticIntervalClass


class MelodicChromaticInterval(_ChromaticInterval, _MelodicInterval):
   '''.. versionaddedd:: 1.1.2

   Melodic chromatic interval in semitones. ::

      abjad> pitchtools.MelodicChromaticInterval(-2)
      MelodicChromaticInterval(-2)
   '''

   def __init__(self, arg):
      if isinstance(arg, (int, float, long)):
         self._number = arg
      elif isinstance(arg, _Interval):
         self._number = arg.semitones
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
      return abs(self.number) >= abs(arg.number)

   def __gt__(self, arg):
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.number) > abs(arg.number)

   def __hash__(self):
      return hash(repr(self))

   def __le__(self, arg):
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.number) <= abs(arg.number)

   def __lt__(self, arg):
      if not isinstance(arg, MelodicChromaticInterval):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.number) < abs(arg.number)

   def __neg__(self):
      return MelodicChromaticInterval(-self._number)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return '%s%s' % (self._direction_symbol, abs(self.number))

   ## PUBLIC ATTRIBUTES ##

   @property
   def direction_number(self):
      return mathtools.sign(self.number) 

   @property
   def harmonic_interval(self):
      number = abs(self.number)
      return HarmonicChromaticInterval(number)

   @property
   def interval_class(self):
      #return self.direction_number * (abs(self.number) % 12)
      return MelodicChromaticIntervalClass(self)
