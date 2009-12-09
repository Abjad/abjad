from abjad.tools.pitchtools._CounterpointInterval import _CounterpointInterval
from abjad.tools.pitchtools._HarmonicInterval import _HarmonicInterval


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
         self._number = token.number
      else:
         raise TypeError('must be number or diatonic interval.')
