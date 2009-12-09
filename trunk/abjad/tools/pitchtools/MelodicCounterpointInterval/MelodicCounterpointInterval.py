from abjad.tools.pitchtools._CounterpointInterval import _CounterpointInterval
from abjad.tools.pitchtools._MelodicInterval import _MelodicInterval


class MelodicCounterpointInterval(_CounterpointInterval, _MelodicInterval):
   '''.. versionadded:: 1.1.2

   Melodic counterpoint interval.
   Like a reduced diatonic interval stripped of major, minor
   or other quality. Similar to the numbers of figured bass.
   '''

   def __init__(self, number):
      if not isinstance(number, int):
         raise TypeError('must be integer.')
      if number == 0:
         raise ValueError('must be nonzero integer.')
      self._number = number
