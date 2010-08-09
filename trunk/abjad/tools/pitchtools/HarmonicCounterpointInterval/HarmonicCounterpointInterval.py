from abjad.tools.pitchtools._CounterpointInterval import _CounterpointInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval
from abjad.tools.pitchtools.HarmonicCounterpointIntervalClass import HarmonicCounterpointIntervalClass


class HarmonicCounterpointInterval(_CounterpointInterval, _HarmonicInterval):
   '''.. versionadded:: 1.1.2

   Harmonic counterpoint interval.
   Like a type of reduced diatonic interval, without major,
   minor, perfect or other quality.
   '''

   def __init__(self, token):
      from abjad.tools.pitchtools._DiatonicInterval import _DiatonicInterval
      if isinstance(token, int):
         if not 0 < token:
            raise ValueError('must be positive integer.')
         self._number = token
      elif isinstance(token, _DiatonicInterval):
         self._number = abs(token.number)
      else:
         raise TypeError('must be number or diatonic interval.')

   ## OVERLOADS ##
   
   def __eq__(self, arg):
      if isinstance(arg, HarmonicCounterpointInterval):
         if self.number == arg.number:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class(self):
      return HarmonicCounterpointIntervalClass(self)
