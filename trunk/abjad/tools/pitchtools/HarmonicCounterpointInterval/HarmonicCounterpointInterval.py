from abjad.tools.pitchtools._CounterpointInterval import _CounterpointInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval


class HarmonicCounterpointInterval(_CounterpointInterval, _HarmonicInterval):
   '''.. versionadded:: 1.1.2

   Harmonic counterpoint interval.
   Like a type of reduced diatonic interval, without major,
   minor, perfect or other quality.
   '''

   def __init__(self, number):
      if not isinstance(number, int):
         raise TypeError('must be integer.')
      if not 0 < number:
         raise ValueError('must be positive integer.')
      self._number = number
