from abjad.tools import mathtools
from abjad.tools.pitchtools._ChromaticInterval import _ChromaticInterval
from abjad.tools.pitchtools._MelodicInterval import _MelodicInterval


class MelodicChromaticInterval(_ChromaticInterval, _MelodicInterval):
   '''.. versionadded:: 1.1.2

   Abjad model of melodic chromatic interval::

      abjad> pitchtools.MelodicChromaticInterval(-14)
      MelodicChromaticInterval(-14)

   Melodic chromatic intervals are immutable.
   '''

   def __new__(klass, arg):
      from abjad.tools import pitchtools
      self = object.__new__(klass)
      if isinstance(arg, (int, float, long)):
         number = arg
      elif isinstance(arg, pitchtools._Interval._Interval):
         number = arg.semitones
      else:
         raise TypeError('%s must be number or interval.' % arg)
      object.__setattr__(self, '_number', number)
      return self

   ## OVERLOADS ##

   def __abs__(self):
      return self.harmonic_chromatic_interval

   def __ge__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.number) >= abs(arg.number)

   def __gt__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.number) > abs(arg.number)

   def __hash__(self):
      return hash(repr(self))

   def __le__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.number) <= abs(arg.number)

   def __lt__(self, arg):
      if not isinstance(arg, type(self)):
         raise TypeError('%s must be melodic chromatic interval.' % arg)
      if not self.direction_number == arg.direction_number:
         raise ValueError(
            'can only compare melodic intervals of same direction.')
      return abs(self.number) < abs(arg.number)

   def __neg__(self):
      return type(self)(-self._number)

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
   def harmonic_chromatic_interval(self):
      from abjad.tools import pitchtools
      number = abs(self.number)
      return pitchtools.HarmonicChromaticInterval(number)

   @property
   #def interval_class(self):
   def melodic_chromatic_interval_class(self):
      from abjad.tools import pitchtools
      return pitchtools.MelodicChromaticIntervalClass(self)
