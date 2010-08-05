from abjad.core import Rational
from abjad.components._Tuplet.FixedDurationTuplet._FixedDurationTupletDurationInterface \
   import _FixedDurationTupletDurationInterface
from abjad.components._Tuplet._Tuplet import _Tuplet


class FixedDurationTuplet(_Tuplet):

   def __init__(self, duration, music):
      _Tuplet.__init__(self, music)
      self._duration = _FixedDurationTupletDurationInterface(self, duration)
      self._signifier = '@'

   ### OVERLOADS ###
 
   def __repr__(self):
      return 'FixedDurationTuplet(%s, [%s])' % (
         self.duration.target, self._summary)

   def __str__(self):
      if len(self) > 0:
         return '{%s %s %s %s}' % (
            self._signifier, self.ratio, self._summary, self._signifier)
      else:
         return '{%s %s %s}' % (
            self._signifier, self.duration.target, self._signifier)

   ### PUBLIC METHODS ###

   def trim(self, start, stop = 'unused'):
      if stop != 'unused':
         assert not (start == 0 and (stop is None or stop >= len(self)))
      old_multiplier = self.duration.multiplier
      if stop == 'unused':
         del(self[start])
      else:
         del(self[start : stop])
      self.duration.target = old_multiplier * self.duration.contents
